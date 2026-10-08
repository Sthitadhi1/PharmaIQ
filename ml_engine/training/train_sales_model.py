import pandas as pd
import numpy as np
from ml_engine.models.sales_forecasting import SalesForecastingModel
from ml_engine.evaluation.model_metrics import calculate_accuracy, calculate_precision
from sklearn.model_selection import train_test_split
from ml_engine.training.paths import SAVED_MODELS_DIR, save_metrics
from sklearn.metrics import mean_squared_error, r2_score


def generate_sample_data(n_samples=200):
    """Generate synthetic sales data for training."""
    np.random.seed(42)
    data = {
        'historical_sales': np.random.randint(10000, 100000, n_samples),
        'marketing_spend': np.random.randint(1000, 50000, n_samples),
        'season': np.random.randint(1, 5, n_samples),  # Q1-Q4
        'region_code': np.random.randint(1, 6, n_samples),  # 5 regions
        'product_category': np.random.randint(1, 4, n_samples),
    }
    df = pd.DataFrame(data)
    # Target was previously random and unrelated to the inputs; model it as growth on
    # historical sales driven by marketing spend and seasonality, plus noise.
    seasonal = df['season'].map({1: 0.95, 2: 1.0, 3: 1.05, 4: 1.12})
    df['forecast_sales'] = (
        df['historical_sales'] * seasonal * (1 + df['marketing_spend'] / 250000)
        + np.random.normal(0, 3000, n_samples)
    ).round().astype(int)
    return df


def train_sales_model(model_path: str = SAVED_MODELS_DIR):
    """Train and evaluate sales forecasting model."""
    print('=== Training Sales Forecasting Model ===')

    # Generate synthetic data
    df = generate_sample_data(n_samples=1000)
    print(f'Generated {len(df)} training samples')

    # Prepare data
    model = SalesForecastingModel(model_path=model_path)
    X = model.prepare_data(df)
    y = df['forecast_sales'].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print('Training ensemble model (Random Forest + XGBoost Regression)...')
    model.train(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f'\nModel Performance Metrics:')
    print(f'  RMSE:  {rmse:.2f}')
    print(f'  R² Score: {r2:.4f}')
    print(f'  Mean Absolute Error: {np.mean(np.abs(y_test - y_pred)):.2f}')

    # Save model
    model.save_models()
    save_metrics('sales_forecast', {'rmse': rmse, 'r2_score': r2, 'mae': np.mean(np.abs(y_test - y_pred)), 'samples': len(df)}, model_path)
    print(f'\nModel saved to {model_path}')

    # Test prediction
    print('\n=== Sample Prediction ===')
    test_features = {
        'historical_sales': 50000,
        'marketing_spend': 15000,
        'season': 2,
        'region_code': 3,
        'product_category': 2
    }
    prediction = model.forecast_sales(test_features)
    print(f'Sales Forecast Prediction: {prediction}')


main = train_sales_model

if __name__ == '__main__':
    train_sales_model()
