from typing import Dict

from fastapi import APIRouter

from app.ai_assistant.analytics_agent import DatasetAnalyst
from app.services import analytics_service
from decision_engine.business_rules import DecisionAnalyzer
from decision_engine.strategy_generator import StrategyGenerator

router = APIRouter(prefix='/api/executive', tags=['Executive'])
analyst = DatasetAnalyst()
decision_analyzer = DecisionAnalyzer()
strategy_generator = StrategyGenerator()


@router.get('/overview')
def executive_overview():
    patients = analytics_service.patient_analytics()
    metrics = analytics_service.model_metrics()
    return {
        'kpis': analytics_service.overview(),
        'revenue_forecast': analytics_service.sales_forecast(),
        'risk_distribution': patients['risk_distribution'],
        'model_performance': {
            name: {key: values.get(key) for key in ('accuracy', 'f1_score', 'r2_score', 'silhouette') if key in values}
            for name, values in metrics.items()
        },
        'recommendations': [item['text'] for item in analytics_service.recommendations()],
    }


@router.get('/insights')
def executive_insights():
    return analyst.answer('Which region generated maximum sales?')


@router.post('/strategy')
def executive_strategy(payload: Dict[str, str]):
    analysis = decision_analyzer.analyze(payload)
    recommendations = strategy_generator.recommend(payload)
    return {
        'business_problem': analysis['business_problem'],
        'region': analysis['region'],
        'recommendations': recommendations
    }
