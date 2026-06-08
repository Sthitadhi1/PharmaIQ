from typing import Any, Dict

import shap


class SHAPExplainer:
    def explain(self, model: Any, data: Any) -> Dict[str, Any]:
        explainer = shap.Explainer(model)
        shap_values = explainer(data)
        return {
            'explanation': shap_values.values.tolist() if hasattr(shap_values, 'values') else [],
            'feature_names': shap_values.feature_names if hasattr(shap_values, 'feature_names' ) else []
        }
