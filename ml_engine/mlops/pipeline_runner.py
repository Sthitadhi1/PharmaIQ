import os
from pathlib import Path
from typing import Dict, Any

import mlflow
import pandas as pd

from ml_engine.models.patient_risk_model import PatientRiskModel
from ml_engine.models.trial_dropout_model import TrialDropoutModel
from ml_engine.models.sales_forecasting import SalesForecastingModel
from ml_engine.models.doctor_segmentation import DoctorSegmentationModel
from ml_engine.preprocessing.data_cleaning import clean_missing_values, remove_duplicates
from ml_engine.preprocessing.feature_engineering import encode_categories, scale_features
from ml_engine.evaluation.model_metrics import (
    calculate_accuracy,
    calculate_precision,
    calculate_recall,
    calculate_f1_score,
    calculate_regression_metrics
)
from ml_engine.mlops.experiment_tracker import ExperimentTracker
from ml_engine.mlops.model_registry import ModelRegistry
from ml_engine.explainability.shap_explainer import SHAPExplainer


class PipelineRunner:
    def __init__(self, raw_dir: str = 'datasets/raw', model_path: str = 'ml_engine/saved_models'):
        self.raw_dir = raw_dir
        self.model_path = model_path
        self.tracker = ExperimentTracker('PharmaIQ')
        self.registry = ModelRegistry()
        self.explainer = SHAPExplainer()

    def _load_csv(self, filename: str) -> pd.DataFrame:
        path = Path(self.raw_dir) / filename
        if not path.exists():
            raise FileNotFoundError(f'Raw dataset not found: {path}')
        df = pd.read_csv(path)
        return df

    def _prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = remove_duplicates(clean_missing_values(df))
        return encode_categories(df_clean, df_clean.select_dtypes(include=['object', 'category']).columns.tolist())

    def run_patient_pipeline(self) -> Dict[str, Any]:
        df = self._prepare(self._load_csv('patients.csv'))
        model = PatientRiskModel(model_path=self.model_path)
        X = model.prepare_data(df)
        y = df['risk_level'].astype(int).values if 'risk_level' in df.columns else df['risk'].astype(int).values
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        model.train(X_train, y_train)
        predictions = (model.predict(X_test) > 0.5).astype(int)
        metrics = {
            'accuracy': calculate_accuracy(y_test, predictions),
            'precision': calculate_precision(y_test, predictions),
            'recall': calculate_recall(y_test, predictions),
            'f1_score': calculate_f1_score(y_test, predictions)
        }
        self.tracker.log_metrics(metrics)
        model.save_models()
        self.registry.register_model(f'{self.model_path}/patient_rf_model.pkl', 'PatientRiskModel')

        explain_data = X_test[:5]
        explanation = self.explainer.explain(model.rf_model, explain_data)
        return {'pipeline': 'patient_risk', 'samples': len(df), 'metrics': metrics, 'explanation': explanation}

    def run_trial_pipeline(self) -> Dict[str, Any]:
        df = self._prepare(self._load_csv('clinical_trials.csv'))
        model = TrialDropoutModel(model_path=self.model_path)
        X = model.prepare_data(df)
        y = df['dropout'].astype(int).values
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        model.train(X_train, y_train)
        predictions = (model.predict(X_test) > 0.5).astype(int)
        metrics = {
            'accuracy': calculate_accuracy(y_test, predictions),
            'precision': calculate_precision(y_test, predictions),
            'recall': calculate_recall(y_test, predictions),
            'f1_score': calculate_f1_score(y_test, predictions)
        }
        self.tracker.log_metrics(metrics)
        model.save_models()
        self.registry.register_model(f'{self.model_path}/trial_rf_model.pkl', 'TrialDropoutModel')

        explain_data = X_test[:5]
        explanation = self.explainer.explain(model.rf_model, explain_data)
        return {'pipeline': 'trial_dropout', 'samples': len(df), 'metrics': metrics, 'explanation': explanation}

    def run_sales_pipeline(self) -> Dict[str, Any]:
        df = self._prepare(self._load_csv('pharma_sales.csv'))
        model = SalesForecastingModel(model_path=self.model_path)
        X = model.prepare_data(df)
        y = df['revenue'].astype(float).values
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        model.train(X_train, y_train)
        predictions = model.predict(X_test)
        metrics = calculate_regression_metrics(y_test, predictions)
        self.tracker.log_metrics(metrics)
        model.save_models()
        self.registry.register_model(f'{self.model_path}/sales_rf_model.pkl', 'SalesForecastingModel')

        explain_data = X_test[:5]
        explanation = self.explainer.explain(model.rf_model, explain_data)
        return {'pipeline': 'sales_forecast', 'samples': len(df), 'metrics': metrics, 'explanation': explanation}

    def run_doctor_pipeline(self) -> Dict[str, Any]:
        df = self._prepare(self._load_csv('doctors.csv'))
        model = DoctorSegmentationModel(model_path=self.model_path)
        X = model.prepare_data(df)
        model.train(X)
        self.tracker.log_metrics({'clusters': model.n_clusters})
        model.save_models()
        self.registry.register_model(f'{self.model_path}/doctor_kmeans_model.pkl', 'DoctorSegmentationModel')

        explanation = {'segments': list(model.segment_labels.values())}
        return {'pipeline': 'doctor_segmentation', 'samples': len(df), 'metrics': {'clusters': model.n_clusters}, 'explanation': explanation}

    def run_all_pipelines(self) -> Dict[str, Any]:
        results = {
            'patient': self.run_patient_pipeline(),
            'trial': self.run_trial_pipeline(),
            'sales': self.run_sales_pipeline(),
            'doctor': self.run_doctor_pipeline()
        }
        return results


if __name__ == '__main__':
    runner = PipelineRunner()
    results = runner.run_all_pipelines()
    print('=== MLOps training pipeline completed ===')
    print(results)
