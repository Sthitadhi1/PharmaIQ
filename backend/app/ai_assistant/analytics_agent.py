"""Answers natural-language analytics questions by computing them live from the CSV datasets."""
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from app.services import analytics_service as analytics


@dataclass
class Metric:
    label: str
    keywords: List[str]
    compute: Callable[[pd.DataFrame], float]
    kind: str  # money | count | pct | ratio | number | days
    additive: bool = False  # sums can be shown as a share of the total


@dataclass
class Domain:
    name: str
    source: str
    frame: Callable[[], pd.DataFrame]
    keywords: List[str]
    primary: List[str]
    dimensions: Dict[str, List[str]]
    filterable: List[str]
    metrics: Dict[str, Metric]
    default_metric: str
    aliases: Dict[str, Dict[str, str]] = field(default_factory=dict)


COUNT_WORDS = ['how many', 'number of', 'count', 'total number']
MAX_WORDS = ['highest', 'maximum', 'max', 'most', 'top', 'best', 'largest', 'biggest', 'leading', 'greatest', 'lead', 'leads']
MIN_WORDS = ['lowest', 'minimum', 'min', 'least', 'worst', 'smallest', 'fewest', 'weakest', 'bottom']
FORECAST_WORDS = ['forecast', 'predict', 'projection', 'project', 'next month', 'next quarter', 'future', 'expected revenue']
OVERVIEW_WORDS = ['summary', 'summarize', 'summarise', 'overview', 'kpi', 'kpis', 'key facts', 'insights', 'dashboard', 'how are we doing']

DOMAINS: List[Domain] = [
    Domain(
        name='sales', source='pharma_sales.csv', frame=analytics.sales_frame,
        keywords=['sale', 'sales', 'revenue', 'sold', 'units', 'medicine', 'drug', 'product', 'marketing', 'roi', 'income', 'earn'],
        primary=['sales', 'revenue', 'medicine', 'drug', 'marketing'],
        dimensions={
            'region': ['region', 'regions', 'territory', 'area'],
            'medicine': ['medicine', 'medicines', 'drug', 'drugs', 'product', 'products'],
            'month': ['month', 'monthly', 'trend'],
            'year': ['year', 'yearly', 'annual', 'annually'],
        },
        filterable=['region', 'medicine', 'year'],
        metrics={
            'roi': Metric('Marketing ROI (revenue per $ of marketing)', ['roi', 'return', 'efficien'],
                          lambda d: d['revenue'].sum() / d['marketing_spend'].sum(), 'ratio'),
            'marketing': Metric('Marketing spend', ['marketing', 'spend', 'spent', 'budget'], lambda d: d['marketing_spend'].sum(), 'money', True),
            'units': Metric('Units sold', ['unit', 'sold', 'volume', 'quantity'], lambda d: d['units_sold'].sum(), 'count', True),
            'revenue': Metric('Revenue', ['revenue', 'sales', 'income', 'earn', 'generated', 'money'], lambda d: d['revenue'].sum(), 'money', True),
        },
        default_metric='revenue',
        aliases={'medicine': {'drug a': 'DrugA', 'drug b': 'DrugB', 'drug c': 'DrugC'}},
    ),
    Domain(
        name='patients', source='patients.csv', frame=analytics.patients_frame,
        keywords=['patient', 'patients', 'risk', 'adherence', 'diabet', 'cholesterol', 'blood pressure', 'admission'],
        primary=['patient', 'patients'],
        dimensions={
            'gender': ['gender', 'sex', 'male', 'female', 'men', 'women'],
            'age_group': ['age group', 'age groups', 'age band', 'by age', 'per age', 'older', 'younger', 'age bracket'],
            'diabetic': ['by diabetes', 'diabetes status', 'diabetic vs', 'diabetics vs'],
            'risk_level': ['risk level', 'risk category', 'by risk', 'risk group'],
        },
        filterable=['gender'],
        metrics={
            'low_risk': Metric('Low-risk patients', ['low risk', 'low - risk'], lambda d: (~d['is_high_risk']).sum(), 'count_rate'),
            'adherence': Metric('Average medication adherence', ['adherence', 'complian'], lambda d: d['medication_adherence'].mean(), 'pct'),
            'admissions': Metric('Average previous admissions', ['admission', 'readmission', 'hospitali'], lambda d: d['previous_admissions'].mean(), 'number'),
            'cholesterol': Metric('Average cholesterol', ['cholesterol'], lambda d: d['cholesterol'].mean(), 'number'),
            'blood_pressure': Metric('Average blood pressure', ['blood pressure', 'bp'], lambda d: d['blood_pressure'].mean(), 'number'),
            'diabetic': Metric('Diabetic patients', ['diabet'], lambda d: d['diabetes'].sum(), 'count_rate'),
            'age': Metric('Average age', ['average age', 'mean age', 'how old'], lambda d: d['age'].mean(), 'number'),
            'high_risk': Metric('High-risk patients', ['high risk', 'high - risk', 'at risk', 'at - risk', 'risky', 'risk'],
                                lambda d: d['is_high_risk'].sum(), 'count_rate'),
            'patients': Metric('Patients', COUNT_WORDS + ['patients'], lambda d: len(d), 'count', True),
        },
        default_metric='patients',
        aliases={'gender': {'male': 'M', 'men': 'M', 'female': 'F', 'women': 'F'}},
    ),
    Domain(
        name='trials', source='clinical_trials.csv', frame=analytics.trials_frame,
        keywords=['trial', 'trials', 'dropout', 'drop out', 'drop-out', 'phase', 'side effect', 'participant', 'attrition', 'retention', 'enrol'],
        primary=['trial', 'trials', 'dropout', 'drop out', 'participant'],
        dimensions={
            'phase': ['phase', 'phases'],
            'side_effects': ['side effect', 'side-effect', 'adverse'],
            'age_group': ['age group', 'by age', 'per age', 'older', 'younger'],
            'duration_group': ['by duration', 'duration group', 'trial length'],
        },
        filterable=['phase', 'side_effects'],
        metrics={
            'completion': Metric('Completion rate', ['completion', 'complete', 'retention', 'retain', 'stay'], lambda d: (1 - d['dropout'].mean()) * 100, 'pct'),
            'dropout': Metric('Dropout rate', ['dropout', 'drop out', 'drop-out', 'dropped', 'attrition', 'quit', 'leave'], lambda d: d['dropout'].mean() * 100, 'pct'),
            'duration': Metric('Average trial duration', ['duration', 'days', 'length', 'how long'], lambda d: d['duration_days'].mean(), 'days'),
            'participants': Metric('Participants', COUNT_WORDS + ['participants'], lambda d: len(d), 'count', True),
        },
        default_metric='dropout',
        aliases={'phase': {'phase 1': 'Phase 1', 'phase 2': 'Phase 2', 'phase 3': 'Phase 3', 'phase i': 'Phase 1',
                           'phase ii': 'Phase 2', 'phase iii': 'Phase 3'}},
    ),
    Domain(
        name='doctors', source='doctors.csv', frame=analytics.doctors_frame,
        keywords=['doctor', 'doctors', 'hcp', 'physician', 'prescriber', 'engagement', 'specialization', 'specialty', 'prescription'],
        primary=['doctor', 'doctors', 'hcp', 'physician', 'prescriber'],
        dimensions={
            'specialization': ['specialization', 'specialisation', 'specialty', 'speciality', 'specialties', 'field'],
            'region': ['region', 'regions', 'territory', 'area'],
            'segment': ['segment', 'segments', 'tier', 'tiers'],
        },
        filterable=['specialization', 'region', 'segment'],
        metrics={
            'sales': Metric('Sales generated', ['sales', 'revenue', 'generate'], lambda d: d['sales_generated'].sum(), 'money', True),
            'prescriptions': Metric('Prescriptions', ['prescription', 'prescribe'], lambda d: d['prescriptions'].sum(), 'count', True),
            'patients_seen': Metric('Patients seen', ['patients seen', 'patient volume', 'see the most patients'], lambda d: d['patients_seen'].sum(), 'count', True),
            'doctors': Metric('Doctors', COUNT_WORDS, lambda d: len(d), 'count', True),
            'engagement': Metric('Average engagement score', ['engagement', 'engaged', 'best', 'active'], lambda d: d['engagement_score'].mean(), 'number'),
        },
        default_metric='engagement',
        aliases={'segment': {'segment a': 'Segment A', 'segment b': 'Segment B', 'segment c': 'Segment C'}},
    ),
]


def fmt(value: float, kind: str, total: Optional[float] = None) -> str:
    if kind == 'money':
        if abs(value) >= 1_000_000:
            return f'${value / 1_000_000:,.2f}M'
        if abs(value) >= 1_000:
            return f'${value / 1_000:,.1f}K'
        return f'${value:,.0f}'
    if kind == 'pct':
        return f'{value:.1f}%'
    if kind == 'ratio':
        return f'{value:.2f}x'
    if kind == 'days':
        return f'{value:,.0f} days'
    if kind == 'count_rate':
        return f'{value:,.0f}' + (f' ({value / total * 100:.1f}%)' if total else '')
    if kind == 'count':
        return f'{value:,.0f}'
    return f'{value:,.1f}'


def _contains(text: str, phrase: str) -> bool:
    """Prefix match at a word start, so 'admission' also finds 'admissions'."""
    return re.search(rf'(?<![a-z0-9]){re.escape(phrase)}', text) is not None


def _word(text: str, phrase: str) -> bool:
    """Whole-word match, so the value 'high' does not match inside 'highest'."""
    return re.search(rf'(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])', text) is not None


class DatasetAnalyst:
    """Rule-based question understanding over the datasets: domain, metric, grouping and filters."""

    def answer(self, question: str) -> Optional[Dict[str, Any]]:
        text = ' '.join(question.lower().replace('?', ' ').replace('-', ' - ').split())
        domain = self._pick_domain(text)
        if domain is None:
            return self._overview() if any(_contains(text, word) for word in OVERVIEW_WORDS) else None
        if domain.name == 'sales' and any(_contains(text, word) for word in FORECAST_WORDS):
            return self._forecast()

        df = domain.frame()
        total_rows = len(df)
        filters = self._filters(domain, df, text)
        for column, value in filters.items():
            df = df[df[column].astype(str) == value]
        if df.empty:
            return self._result(domain, 'No records match those filters.', None, filters)

        metric_key = next((key for key, metric in domain.metrics.items()
                           if any(_contains(text, word) for word in metric.keywords)), domain.default_metric)
        metric = domain.metrics[metric_key]
        group = next((dim for dim, words in domain.dimensions.items()
                      if dim not in filters and any(_contains(text, word) for word in words)), None)
        if group is None and domain.name == 'sales' and _contains(text, 'trend'):
            group = 'month'

        if group:
            return self._grouped(domain, df, metric, group, text, filters)
        value = metric.compute(df)
        scope = self._scope(filters)
        answer = f'{metric.label}{scope}: {fmt(value, metric.kind, len(df))}'
        if filters and metric.kind not in ('count', 'count_rate'):
            answer += f' (vs {fmt(metric.compute(domain.frame()), metric.kind, total_rows)} across all records)'
        answer += f'. Based on {len(df):,} records in {domain.source}.'
        return self._result(domain, answer, None, filters)

    # ---- understanding ----

    def _pick_domain(self, text: str) -> Optional[Domain]:
        best, best_score = None, 0
        for domain in DOMAINS:
            score = sum(_contains(text, word) for word in domain.keywords) + 2 * sum(_contains(text, word) for word in domain.primary)
            if score > best_score:
                best, best_score = domain, score
        return best

    def _filters(self, domain: Domain, df: pd.DataFrame, text: str) -> Dict[str, str]:
        filters: Dict[str, str] = {}
        for column in domain.filterable:
            for phrase, value in domain.aliases.get(column, {}).items():
                if _word(text, phrase):
                    filters[column] = value
            if column in filters:
                continue
            for value in df[column].astype(str).unique():
                if len(value) > 1 and _word(text, value.lower()):
                    filters[column] = value
                    break
        return filters

    @staticmethod
    def _scope(filters: Dict[str, str]) -> str:
        return (' for ' + ', '.join(filters.values())) if filters else ''

    # ---- answers ----

    def _grouped(self, domain: Domain, df: pd.DataFrame, metric: Metric, group: str, text: str, filters: Dict[str, str]):
        rows = []
        for name, part in df.groupby(group, observed=True):
            rows.append({'group': str(name), 'value': float(metric.compute(part)), 'records': len(part)})
        if group == 'month':
            rows.sort(key=lambda row: row['group'])
        ascending = any(_word(text, word) for word in MIN_WORDS)
        def rank_key(row):
            return row['value'] / row['records'] if metric.kind == 'count_rate' else row['value']

        ranked = sorted(rows, key=rank_key, reverse=not ascending)
        total = sum(row['value'] for row in rows)
        rate_base = {row['group']: row['records'] for row in rows}

        def show(row):
            if metric.kind == 'count_rate':
                return fmt(row['value'], metric.kind, rate_base[row['group']])
            return fmt(row['value'], metric.kind)

        label = group.replace('_', ' ')
        scope = self._scope(filters)
        top = ranked[0]
        if group == 'month':
            best = max(rows, key=lambda row: row['value'])
            first, last = rows[0], rows[-1]
            answer = (f'{metric.label}{scope} by month, {first["group"]} to {last["group"]}: best month {best["group"]} '
                      f'({show(best)}); latest month {last["group"]} ({show(last)}).')
        elif any(_word(text, word) for word in MAX_WORDS + MIN_WORDS) or text.startswith(('which', 'what', 'who')):
            share = f', {top["value"] / total * 100:.1f}% of the total' if metric.additive and total else ''
            direction = 'lowest' if ascending else 'highest'
            noun = metric.label[0].lower() + metric.label[1:]
            answer = (f'{top["group"]} has the {direction} {noun}{scope}: {show(top)}{share}. '
                      f'Next: ' + ', '.join(f'{row["group"]} ({show(row)})' for row in ranked[1:4]) + '.')
        else:
            answer = f'{metric.label}{scope} by {label}: ' + ', '.join(f'{row["group"]} {show(row)}' for row in ranked[:8]) + '.'
        answer += f' Computed from {sum(rate_base.values()):,} records in {domain.source}.'

        table_rows = rows if group == 'month' else ranked
        table = {
            'columns': [label.capitalize(), metric.label, 'Records'],
            'rows': [[row['group'], show(row), row['records']] for row in table_rows],
        }
        return self._result(domain, answer, table, filters)

    def _forecast(self):
        forecast = analytics.sales_forecast()
        months = ', '.join(f'{item["month"]}: {fmt(item["revenue"], "money")}' for item in forecast['forecast'])
        trend = forecast['monthly_trend']
        answer = (f'Revenue forecast for the next 3 months: {months} (total {fmt(forecast["next_3_months_revenue"], "money")}). '
                  f'The trend is {"+" if trend >= 0 else "−"}{fmt(abs(trend), "money")} per month. Method: {forecast["method"]}.')
        table = {'columns': ['Month', 'Forecast revenue'], 'rows': [[item['month'], fmt(item['revenue'], 'money')] for item in forecast['forecast']]}
        return {'answer': answer, 'table': table, 'sources': ['pharma_sales.csv'], 'domain': 'sales'}

    def _overview(self):
        o = analytics.overview()
        facts = [
            ['Patients', f'{o["total_patients"]:,}', f'{o["high_risk_patients"]:,} high risk ({o["high_risk_pct"]}%)'],
            ['Trial participants', f'{o["trial_participants"]:,}', f'dropout rate {o["trial_dropout_rate"]}%'],
            ['Total revenue', fmt(o['total_revenue'], 'money'), f'recent growth {o["recent_growth_pct"]}%'],
            ['Revenue forecast (3 months)', fmt(o['revenue_forecast_3m'], 'money'), 'linear trend'],
            ['Doctors', f'{o["total_doctors"]:,}', f'{o["high_value_doctors"]} high-value; avg engagement {o["avg_engagement"]}'],
        ]
        answer = ('Key facts from the current data: ' + '; '.join(f'{name} {value} ({note})' for name, value, note in facts) + '.')
        return {'answer': answer, 'table': {'columns': ['Measure', 'Value', 'Detail'], 'rows': facts},
                'sources': ['patients.csv', 'clinical_trials.csv', 'pharma_sales.csv', 'doctors.csv'], 'domain': 'overview'}

    @staticmethod
    def _result(domain: Domain, answer: str, table: Optional[dict], filters: Dict[str, str]):
        return {'answer': answer, 'table': table, 'sources': [domain.source], 'domain': domain.name, 'filters': filters}


EXAMPLE_QUESTIONS = [
    'Which region generated maximum sales?',
    'Which medicine has the best ROI?',
    'Forecast revenue for the next 3 months',
    'How many high-risk patients are there?',
    'High-risk share by age group',
    'Which trial phase has the highest dropout rate?',
    'Dropout rate for high side effects',
    'Which specialization has the highest doctor engagement?',
    'Give me a summary of the business',
]
