from typing import Dict

import numpy as np

from app.services.analytics_service import sales_frame

RECENT_DAYS = 90
PSI_WARNING = 0.1
PSI_ALERT = 0.2


def population_stability_index(baseline: np.ndarray, recent: np.ndarray, bins: int = 10) -> float:
    edges = np.unique(np.quantile(baseline, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    expected = np.histogram(baseline, edges)[0] / len(baseline)
    actual = np.histogram(recent, edges)[0] / len(recent)
    expected, actual = np.clip(expected, 1e-6, None), np.clip(actual, 1e-6, None)
    return float(np.sum((actual - expected) * np.log(actual / expected)))


class DriftDetector:
    """Data drift on daily revenue: last 90 days vs everything before (PSI)."""

    def detect(self) -> Dict[str, object]:
        df = sales_frame().sort_values('date')
        cutoff = df['date'].max() - np.timedelta64(RECENT_DAYS, 'D')
        baseline = df[df['date'] <= cutoff]['revenue'].to_numpy(dtype=float)
        recent = df[df['date'] > cutoff]['revenue'].to_numpy(dtype=float)
        psi = population_stability_index(baseline, recent)
        status = 'Drift' if psi >= PSI_ALERT else 'Monitor' if psi >= PSI_WARNING else 'Healthy'
        return {
            'dataset': 'pharma_sales.csv',
            'feature': 'daily revenue',
            'method': f'Population Stability Index, last {RECENT_DAYS} days vs earlier baseline',
            'psi': round(psi, 4),
            'drift': f'{psi:.3f} PSI',
            'baseline_days': int(len(baseline)),
            'recent_days': int(len(recent)),
            'status': status,
        }
