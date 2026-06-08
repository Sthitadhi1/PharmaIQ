import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import os


class SalesForecastingModel:
    """
    Sales Forecasting Model using ensemble methods.
    Combines Random Forest Regression and XGBoost for robust sales predictions.
    ARIMA can be implemented separately for time-series specific data.
    """

    def __init__(self, model_path: str = 'ml_engine/saved_models/'):
        self.model_path = model_path
        self.rf_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'historical_sales', 'marketing_spend', 'season', 'region_code', 'product_category'
        ]

    def prepare_data(self, df: pd.DataFrame):
        """Prepare and scale data for model training."""
        X = df[self.feature_names].values
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train Random Forest and XGBoost regression models."""
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15)
        self.rf_model.fit(X, y)

        self.xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42, max_depth=8)
        self.xgb_model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Ensemble prediction combining RF and XGBoost.
        Returns average predictions.
        """
        if self.rf_model is None or self.xgb_model is None:
            raise ValueError('Models not trained. Call train() first or load_models().')

        rf_pred = self.rf_model.predict(X)
        xgb_pred = self.xgb_model.predict(X)

        # Ensemble: average of both models
        ensemble_pred = (rf_pred + xgb_pred) / 2
        return ensemble_pred

    def forecast_sales(self, features: dict) -> dict:
        """
        Forecast future sales from feature dictionary.
        Returns sales forecast and growth percentage.
        """
        X = np.array([[
            features.get('historical_sales', 10000),
            features.get('marketing_spend', 5000),
            features.get('season', 1),  # 1-4 for quarters
            features.get('region_code', 1),
            features.get('product_category', 1)
        ]])

        X_scaled = self.scaler.transform(X)
        forecast_sales = self.predict(X_scaled)[0]
        historical = features.get('historical_sales', 10000)
        growth = ((forecast_sales - historical) / historical) * 100 if historical > 0 else 0

        return {
            'forecast_sales': round(float(forecast_sales), 2),
            'growth_percentage': round(float(growth), 2),
            'confidence': 'High' if abs(growth) < 50 else 'Medium'
        }

    def save_models(self):
        """Save trained models to disk."""
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.rf_model, os.path.join(self.model_path, 'sales_rf_model.pkl'))
        joblib.dump(self.xgb_model, os.path.join(self.model_path, 'sales_xgb_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'sales_scaler.pkl'))

    def load_models(self):
        """Load trained models from disk."""
        self.rf_model = joblib.load(os.path.join(self.model_path, 'sales_rf_model.pkl'))
        self.xgb_model = joblib.load(os.path.join(self.model_path, 'sales_xgb_model.pkl'))
        self.scaler = joblib.load(os.path.join(self.model_path, 'sales_scaler.pkl'))
