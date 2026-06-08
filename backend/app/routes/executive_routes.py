from fastapi import APIRouter
from typing import Dict
from app.ai_assistant.analytics_agent import AnalyticsAgent
from decision_engine.business_rules import DecisionAnalyzer
from decision_engine.strategy_generator import StrategyGenerator

router = APIRouter(prefix='/api/executive', tags=['Executive'])
agent = AnalyticsAgent()
decision_analyzer = DecisionAnalyzer()
strategy_generator = StrategyGenerator()


@router.get('/overview')
def executive_overview():
    return {
        'revenue_forecast': 4.8,
        'risk_distribution': {'low': 30, 'medium': 45, 'high': 25},
        'model_performance': {
            'patient_risk': {'accuracy': 0.92, 'f1_score': 0.88},
            'trial_dropout': {'accuracy': 0.89, 'f1_score': 0.84}
        },
        'recommendations': [
            'Expand high-value doctor engagement in region 3',
            'Prioritize patient adherence programs for medium-risk cohorts',
            'Increase pharma marketing in emerging regional clusters'
        ]
    }


@router.get('/insights')
def executive_insights():
    return agent.analyze_question('Which region generated maximum sales?', {})


@router.post('/strategy')
def executive_strategy(payload: Dict[str, str]):
    analysis = decision_analyzer.analyze(payload)
    recommendations = strategy_generator.recommend(payload)
    return {
        'business_problem': analysis['business_problem'],
        'region': analysis['region'],
        'recommendations': recommendations
    }
