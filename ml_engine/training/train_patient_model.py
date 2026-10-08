import pandas as pd
import numpy as np
from ml_engine.models.patient_risk_model import PatientRiskModel
from ml_engine.evaluation.model_metrics import calculate_accuracy, calculate_precision, calculate_recall, calculate_f1_score
from sklearn.model_selection import train_test_split
from ml_engine.training.paths import SAVED_MODELS_DIR, save_metrics


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
    }
    df = pd.DataFrame(data)
    # Labels were previously random (np.random.randint), so the model could only learn
    # noise (~50% accuracy). Derive them from clinically plausible drivers plus noise.
    signal = (
        (df['age'] - 50) / 15
        + (df['glucose_level'] - 135) / 35
        + (df['blood_pressure_systolic'] - 140) / 25
        + (df['previous_visits'] - 10) / 8
    )
    df['risk'] = (signal + np.random.normal(0, 0.8, n_samples) > 0).astype(int)  # 0=Low, 1=High
    return df


def train_patient_model(model_path: str = SAVED_MODELS_DIR):
    """Train and evaluate patient risk model."""
    print('=== Training Patient Risk Prediction Model ===')

    # Generate synthetic data
    df = generate_sample_data(n_samples=1000)
    print(f'Generated {len(df)} training samples')

    # Prepare data
    model = PatientRiskModel(model_path=model_path)
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
    save_metrics('patient_risk', {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1_score': f1, 'samples': len(df)}, model_path)
    print(f'\nModel saved to {model_path}')

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


main = train_patient_model

if __name__ == '__main__':
    train_patient_model()
