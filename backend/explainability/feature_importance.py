from typing import List, Dict


def calculate_top_features(features: Dict[str, float]) -> List[Dict[str, str]]:
    sorted_features = sorted(features.items(), key=lambda item: abs(item[1]), reverse=True)
    return [{'feature': name, 'impact': f"{round(abs(value) * 100)}%"} for name, value in sorted_features[:3]]
