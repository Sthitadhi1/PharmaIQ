from typing import Dict


class DecisionAnalyzer:
    def analyze(self, inputs: Dict[str, str]) -> Dict[str, str]:
        problem = 'Clinical trial retention risk detected' if inputs.get('trial_dropout', '').lower() == 'high' else 'Business action required'
        region = inputs.get('region', 'Unknown')
        return {
            'business_problem': problem,
            'region': region,
            'summary': f'{problem} in region {region}'
        }
