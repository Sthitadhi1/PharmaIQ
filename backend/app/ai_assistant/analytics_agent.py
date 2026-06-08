from typing import Any, Dict


class AnalyticsAgent:
    def analyze_question(self, question: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'region' in question.lower() and 'sales' in question.lower():
            return {
                'insight': 'Regional sales vary by demand and marketing spend.',
                'suggestion': 'Focus promotions in the highest-growth region.'
            }
        return {
            'insight': 'AI assistant can connect business questions to KPIs and model outputs.',
            'suggestion': 'Upload documents or ask clinical and sales questions.'
        }
