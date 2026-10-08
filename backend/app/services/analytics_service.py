"""Aggregates computed live from the CSV datasets; every dashboard number comes from here."""
import json
import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from app.database.config import MODEL_PATH
from app.services.data_service import datasets_last_updated, load_dataset

AGE_BINS = [0, 30, 45, 60, 75, 200]
AGE_LABELS = ['18–29', '30–44', '45–59', '60–74', '75+']
DURATION_BINS = [0, 90, 180, 365, 100000]
DURATION_LABELS = ['< 3 months', '3–6 months', '6–12 months', '12+ months']
SEGMENT_A_MIN = 80
SEGMENT_B_MIN = 60


def _round(value: float, digits: int = 1) -> float:
    return round(float(value), digits)


def _records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    return json.loads(df.to_json(orient='records'))


def segment_label(score: float) -> str:
    if score >= SEGMENT_A_MIN:
        return 'Segment A'
    if score >= SEGMENT_B_MIN:
        return 'Segment B'
    return 'Segment C'


# ---------- enriched datasets ----------

def patients_frame() -> pd.DataFrame:
    df = load_dataset('patients')
    df['age_group'] = pd.cut(df['age'], AGE_BINS, labels=AGE_LABELS, right=False).astype(str)
    df['is_high_risk'] = df['risk_level'].str.upper().eq('HIGH')
    df['diabetic'] = np.where(df['diabetes'] == 1, 'Diabetic', 'Not diabetic')
    return df


def trials_frame() -> pd.DataFrame:
    df = load_dataset('trials')
    df['phase'] = 'Phase ' + df['trial_phase'].astype(int).astype(str)
    df['age_group'] = pd.cut(df['age'], AGE_BINS, labels=AGE_LABELS, right=False).astype(str)
    df['duration_group'] = pd.cut(df['duration_days'], DURATION_BINS, labels=DURATION_LABELS, right=False).astype(str)
    return df


def sales_frame() -> pd.DataFrame:
    df = load_dataset('sales')
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    df['year'] = df['date'].dt.year.astype(str)
    return df


def doctors_frame() -> pd.DataFrame:
    df = load_dataset('doctors')
    df['segment'] = df['engagement_score'].apply(segment_label)
    return df


# ---------- per-domain analytics ----------

def patient_analytics() -> Dict[str, Any]:
    df = patients_frame()
    by_age = df.groupby('age_group', observed=True).agg(patients=('patient_id', 'count'), high_risk=('is_high_risk', 'sum'))
    by_age = by_age.reindex(AGE_LABELS).dropna().reset_index()
    by_age['high_risk_pct'] = (by_age['high_risk'] / by_age['patients'] * 100).round(1)
    by_risk = df.groupby('risk_level').agg(
        patients=('patient_id', 'count'),
        avg_adherence=('medication_adherence', 'mean'),
        avg_admissions=('previous_admissions', 'mean'),
        avg_cholesterol=('cholesterol', 'mean'),
        avg_blood_pressure=('blood_pressure', 'mean'),
    ).round(1).reset_index()
    return {
        'total_patients': int(len(df)),
        'high_risk_patients': int(df['is_high_risk'].sum()),
        'high_risk_pct': _round(df['is_high_risk'].mean() * 100),
        'avg_age': _round(df['age'].mean()),
        'avg_adherence': _round(df['medication_adherence'].mean()),
        'diabetic_pct': _round(df['diabetes'].mean() * 100),
        'risk_distribution': [{'name': row['risk_level'], 'value': int(row['patients'])} for _, row in by_risk.iterrows()],
        'by_age_group': _records(by_age),
        'by_risk_level': _records(by_risk),
        'by_gender': _records(df.groupby('gender').agg(patients=('patient_id', 'count'), high_risk=('is_high_risk', 'sum')).reset_index()),
    }


def trial_analytics() -> Dict[str, Any]:
    df = trials_frame()

    def grouped(column: str, order: List[str] = None):
        table = df.groupby(column, observed=True).agg(participants=('trial_id', 'count'), dropouts=('dropout', 'sum')).reset_index()
        if order:
            table = table.set_index(column).reindex(order).dropna().reset_index()
        table['dropout_rate'] = (table['dropouts'] / table['participants'] * 100).round(1)
        table['completion_rate'] = (100 - table['dropout_rate']).round(1)
        return _records(table)

    return {
        'participants': int(len(df)),
        'active_participants': int((df['dropout'] == 0).sum()),
        'dropouts': int(df['dropout'].sum()),
        'dropout_rate': _round(df['dropout'].mean() * 100),
        'completion_rate': _round((1 - df['dropout'].mean()) * 100),
        'avg_duration_days': _round(df['duration_days'].mean()),
        'high_side_effect_participants': int(df['side_effects'].str.upper().eq('HIGH').sum()),
        'by_phase': grouped('phase'),
        'by_side_effects': grouped('side_effects', ['LOW', 'MEDIUM', 'HIGH']),
        'by_duration': grouped('duration_group', DURATION_LABELS),
        'by_age_group': grouped('age_group', AGE_LABELS),
    }


def _monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.groupby('month').agg(
        revenue=('revenue', 'sum'), units=('units_sold', 'sum'),
        marketing=('marketing_spend', 'sum'), days=('date', 'nunique')
    ).reset_index()
    last = df['date'].max()
    monthly['complete'] = True
    if last.day < last.days_in_month:
        monthly.loc[monthly.index[-1], 'complete'] = False
    return monthly


def sales_forecast(months_ahead: int = 3) -> Dict[str, Any]:
    """Linear trend on the last 12 complete months of revenue."""
    monthly = _monthly_sales(sales_frame())
    history = monthly[monthly['complete']].tail(12)
    x = np.arange(len(history))
    slope, intercept = np.polyfit(x, history['revenue'].to_numpy(dtype=float), 1)
    last_month = pd.Period(history['month'].iloc[-1], freq='M')
    forecast = [
        {'month': str(last_month + step), 'revenue': _round(max(intercept + slope * (len(history) - 1 + step), 0), 0)}
        for step in range(1, months_ahead + 1)
    ]
    return {
        'method': 'Linear trend over the last 12 complete months',
        'monthly_trend': _round(slope, 0),
        'forecast': forecast,
        'next_3_months_revenue': _round(sum(item['revenue'] for item in forecast), 0),
    }


def sales_analytics() -> Dict[str, Any]:
    df = sales_frame()
    monthly = _monthly_sales(df)

    def grouped(column: str):
        table = df.groupby(column).agg(
            revenue=('revenue', 'sum'), units=('units_sold', 'sum'), marketing=('marketing_spend', 'sum')
        ).reset_index()
        table['roi'] = (table['revenue'] / table['marketing']).round(2)
        table['share_pct'] = (table['revenue'] / table['revenue'].sum() * 100).round(1)
        return _records(table.sort_values('revenue', ascending=False))

    complete = monthly[monthly['complete']]
    recent, previous = complete.tail(3)['revenue'].sum(), complete.iloc[-6:-3]['revenue'].sum()
    return {
        'total_revenue': _round(df['revenue'].sum(), 0),
        'total_units': int(df['units_sold'].sum()),
        'total_marketing': _round(df['marketing_spend'].sum(), 0),
        'roi': _round(df['revenue'].sum() / df['marketing_spend'].sum(), 2),
        'recent_growth_pct': _round((recent - previous) / previous * 100) if previous else 0.0,
        'period': {'start': df['date'].min().strftime('%Y-%m-%d'), 'end': df['date'].max().strftime('%Y-%m-%d')},
        'monthly': _records(monthly[['month', 'revenue', 'units', 'marketing', 'complete']]),
        'by_region': grouped('region'),
        'by_medicine': grouped('medicine'),
        'forecast': sales_forecast(),
    }


def doctor_analytics() -> Dict[str, Any]:
    df = doctors_frame()

    def grouped(column: str):
        table = df.groupby(column).agg(
            doctors=('doctor_id', 'count'), avg_engagement=('engagement_score', 'mean'),
            sales=('sales_generated', 'sum'), prescriptions=('prescriptions', 'sum')
        ).reset_index()
        table['avg_engagement'] = table['avg_engagement'].round(1)
        return _records(table.sort_values('sales', ascending=False))

    top = df.sort_values('sales_generated', ascending=False).head(10)
    return {
        'total_doctors': int(len(df)),
        'avg_engagement': _round(df['engagement_score'].mean()),
        'total_sales_generated': _round(df['sales_generated'].sum(), 0),
        'high_value_doctors': int((df['segment'] == 'Segment A').sum()),
        'segments': grouped('segment'),
        'by_specialization': grouped('specialization'),
        'by_region': grouped('region'),
        'top_doctors': _records(top[['doctor_id', 'specialization', 'region', 'engagement_score', 'sales_generated', 'segment']]),
    }


# ---------- cross-domain ----------

def model_metrics() -> Dict[str, Any]:
    path = os.path.join(MODEL_PATH, 'metrics.json')
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def recommendations() -> List[Dict[str, str]]:
    patients, trials, sales, doctors = patient_analytics(), trial_analytics(), sales_analytics(), doctor_analytics()
    top_region = sales['by_region'][0]
    best_roi = max(sales['by_medicine'], key=lambda row: row['roi'])
    worst_phase = max(trials['by_phase'], key=lambda row: row['dropout_rate'])
    worst_side = max(trials['by_side_effects'], key=lambda row: row['dropout_rate'])
    oldest = max(patients['by_age_group'], key=lambda row: row['high_risk_pct'])
    weakest_region = min(doctors['by_region'], key=lambda row: row['avg_engagement'])
    high_risk = next((row for row in patients['by_risk_level'] if row['risk_level'].upper() == 'HIGH'), None)
    low_risk = next((row for row in patients['by_risk_level'] if row['risk_level'].upper() != 'HIGH'), None)

    items = [
        {'area': 'Sales', 'text': f"{top_region['region']} leads with {top_region['share_pct']}% of revenue; protect stock and field coverage there."},
        {'area': 'Sales', 'text': f"{best_roi['medicine']} has the best marketing return ({best_roi['roi']}x revenue per $ spent); shift budget toward it."},
        {'area': 'Clinical', 'text': f"{worst_phase['phase']} has the highest dropout ({worst_phase['dropout_rate']}%); add follow-up visits for its participants."},
        {'area': 'Clinical', 'text': f"Participants with {worst_side['side_effects'].lower()} side effects drop out at {worst_side['dropout_rate']}%; prioritise side-effect management."},
        {'area': 'Patients', 'text': f"Age group {oldest['age_group']} has the highest high-risk share ({oldest['high_risk_pct']}%); target it with preventive programmes."},
        {'area': 'Doctors', 'text': f"{weakest_region['region']} has the lowest doctor engagement ({weakest_region['avg_engagement']}); plan HCP outreach there."},
    ]
    if high_risk and low_risk:
        items.append({'area': 'Patients', 'text': (
            f"High-risk patients average {high_risk['avg_admissions']} prior admissions vs {low_risk['avg_admissions']} for others; "
            'flag frequent re-admissions early.'
        )})
    return items


def overview() -> Dict[str, Any]:
    patients, trials, sales, doctors = patient_analytics(), trial_analytics(), sales_analytics(), doctor_analytics()
    return {
        'total_patients': patients['total_patients'],
        'high_risk_patients': patients['high_risk_patients'],
        'high_risk_pct': patients['high_risk_pct'],
        'trial_participants': trials['participants'],
        'active_trial_participants': trials['active_participants'],
        'trial_dropout_rate': trials['dropout_rate'],
        'total_revenue': sales['total_revenue'],
        'revenue_forecast_3m': sales['forecast']['next_3_months_revenue'],
        'recent_growth_pct': sales['recent_growth_pct'],
        'total_doctors': doctors['total_doctors'],
        'avg_engagement': doctors['avg_engagement'],
        'high_value_doctors': doctors['high_value_doctors'],
        'last_updated': datasets_last_updated(),
    }
