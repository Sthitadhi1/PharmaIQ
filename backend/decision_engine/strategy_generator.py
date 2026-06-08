from typing import Dict, List


class StrategyGenerator:
    def recommend(self, inputs: Dict[str, str]) -> List[str]:
        recommendations = []
        if inputs.get('trial_dropout', '').lower() == 'high':
            recommendations.extend([
                'Increase patient follow-up frequency',
                'Review trial site operations'
            ])
        if inputs.get('region', '').lower() == 'chennai':
            recommendations.append('Deploy targeted regional retention programs')
        if not recommendations:
            recommendations.append('Review the current process and gather additional intelligence')
        return recommendations
