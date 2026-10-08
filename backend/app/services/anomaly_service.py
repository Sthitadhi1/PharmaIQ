"""Statistical anomaly detection over the live datasets."""
from typing import Any, Dict

import numpy as np

from app.services.analytics_service import patients_frame, sales_frame, trials_frame

SALES_Z_THRESHOLD = 3.0
# 99th percentile of the chi-square distribution with 5 degrees of freedom.
PATIENT_MAHALANOBIS_THRESHOLD = 15.086
TRIAL_Z_THRESHOLD = 1.96
PATIENT_FEATURES = ['age', 'blood_pressure', 'cholesterol', 'previous_admissions', 'medication_adherence']


def sales_anomalies() -> Dict[str, Any]:
    """Days whose revenue or units sit more than 3 standard deviations from the mean."""
    df = sales_frame()
    items = []
    for column in ('revenue', 'units_sold'):
        z = (df[column] - df[column].mean()) / df[column].std()
        for index in df.index[z.abs() >= SALES_Z_THRESHOLD]:
            items.append({
                'date': df.at[index, 'date'].strftime('%Y-%m-%d'), 'region': df.at[index, 'region'],
                'medicine': df.at[index, 'medicine'], 'metric': column,
                'value': float(df.at[index, column]), 'z_score': round(float(z[index]), 2),
            })
    return _result('sales', f'|z| >= {SALES_Z_THRESHOLD} on daily revenue and units', len(df), items)


def patient_anomalies() -> Dict[str, Any]:
    """Patients whose combined clinical profile is unusual (Mahalanobis distance, p < 0.01)."""
    df = patients_frame()
    values = df[PATIENT_FEATURES].to_numpy(dtype=float)
    centered = values - values.mean(axis=0)
    inverse_cov = np.linalg.pinv(np.cov(values, rowvar=False))
    distance = np.einsum('ij,jk,ik->i', centered, inverse_cov, centered)
    flagged = df.assign(distance=distance)[distance >= PATIENT_MAHALANOBIS_THRESHOLD].sort_values('distance', ascending=False)
    items = [
        {'patient_id': int(row.patient_id), 'distance': round(float(row.distance), 2), 'risk_level': row.risk_level,
         **{feature: float(getattr(row, feature)) for feature in PATIENT_FEATURES}}
        for row in flagged.itertuples()
    ]
    return _result('patient', 'Mahalanobis distance over 5 clinical features, p < 0.01', len(df), items)


def trial_anomalies() -> Dict[str, Any]:
    """Trial groups whose dropout rate differs significantly from the overall rate (two-sided z-test)."""
    df = trials_frame()
    overall = df['dropout'].mean()
    items = []
    for column in ('phase', 'side_effects', 'duration_group', 'age_group'):
        for group, rows in df.groupby(column, observed=True):
            n = len(rows)
            rate = rows['dropout'].mean()
            z = (rate - overall) / np.sqrt(overall * (1 - overall) / n)
            if abs(z) >= TRIAL_Z_THRESHOLD:
                items.append({'dimension': column, 'group': str(group), 'participants': n,
                              'dropout_rate': round(rate * 100, 1), 'overall_rate': round(overall * 100, 1), 'z_score': round(float(z), 2)})
    return _result('trial', f'Dropout rate differs from overall with |z| >= {TRIAL_Z_THRESHOLD}', len(df), items)


def _result(kind: str, method: str, checked: int, items: list) -> Dict[str, Any]:
    return {
        'type': kind,
        'anomaly': bool(items),
        'count': len(items),
        'records_checked': checked,
        'method': method,
        'message': f'{len(items)} anomalies detected.' if items else 'No anomalies detected in the current data.',
        'items': items[:50],
    }
