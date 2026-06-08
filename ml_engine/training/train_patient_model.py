import pandas as pd
import numpy as np
from ml_engine.models.patient_risk_model import PatientRiskModel
from ml_engine.evaluation.model_metrics import calculate_accuracy, calculate_precision, calculate_recall, calculate_f1_score
from sklearn.model_selection import train_test_split


def generate_sample_data(n_samples=200):
    """Generate synthetic patient risk data for training."""
    np.random.seed(42)
    data = {
        'age': np.random.randint(20, 80, n_samples),
        'previous_visits': np.random.randint(0, 20, n_samples),
        'treatment_duration': np.random.randint(0, 100, n_samples),
        'glucose_level': np.random.randint(70, 200, n_samples),
        'blood_pressure_systolic': np.random.randint(100, 180, n_samples),
        'blood_pressure_diastolic': np.random.randint(60, 120, n_samples),
        'risk': np.random.randint(0, 2, n_samples)  # Binary: 0=Low, 1=High
    }
    return pd.DataFrame(data)


def train_patient_model():
    """Train and evaluate patient risk model."""
    print('=== Training Patient Risk Prediction Model ===')

    # Generate synthetic data
    df = generate_sample_data(n_samples=200)
    print(f'Generated {len(df)} training samples')

    # Prepare data
    model = PatientRiskModel()
    X = model.prepare_data(df)
    y = df['risk'].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print('Training ensemble model (Random Forest, Logistic Regression, XGBoost)...')
    model.train(X_train, y_train)

    # Evaluate
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    accuracy = calculate_accuracy(y_test, y_pred)
    precision = calculate_precision(y_test, y_pred)
    recall = calculate_recall(y_test, y_pred)
    f1 = calculate_f1_score(y_test, y_pred)

    print(f'\nModel Performance Metrics:')
    print(f'  Accuracy:  {accuracy:.4f}')
    print(f'  Precision: {precision:.4f}')
    print(f'  Recall:    {recall:.4f}')
    print(f'  F1 Score:  {f1:.4f}')

    # Save model
    model.save_models()
    print('\nModel saved to ml_engine/saved_models/')

    # Test prediction
    print('\n=== Sample Prediction ===')
    test_features = {
        'age': 55,
        'previous_visits': 5,
        'treatment_duration': 30,
        'glucose_level': 150,
        'blood_pressure_systolic': 140,
        'blood_pressure_diastolic': 90
    }
    prediction = model.predict_risk_level(test_features)
    print(f'Patient Risk Prediction: {prediction}')


if __name__ == '__main__':
    train_patient_model()
