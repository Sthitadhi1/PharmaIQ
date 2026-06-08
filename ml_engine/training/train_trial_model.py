import pandas as pd
import numpy as np
from ml_engine.models.trial_dropout_model import TrialDropoutModel
from ml_engine.evaluation.model_metrics import calculate_accuracy, calculate_precision, calculate_recall, calculate_f1_score
from sklearn.model_selection import train_test_split


def generate_sample_data(n_samples=200):
    """Generate synthetic trial dropout data for training."""
    np.random.seed(42)
    data = {
        'patient_age': np.random.randint(20, 80, n_samples),
        'trial_duration': np.random.randint(1, 36, n_samples),
        'previous_participation': np.random.randint(0, 5, n_samples),
        'side_effects_severity': np.random.randint(0, 10, n_samples),
        'health_score': np.random.randint(40, 100, n_samples),
        'visit_compliance': np.random.randint(50, 100, n_samples),
        'dropout': np.random.randint(0, 2, n_samples)  # Binary: 0=Stayed, 1=Dropout
    }
    return pd.DataFrame(data)


def train_trial_model():
    """Train and evaluate trial dropout prediction model."""
    print('=== Training Clinical Trial Dropout Prediction Model ===')

    # Generate synthetic data
    df = generate_sample_data(n_samples=200)
    print(f'Generated {len(df)} training samples')

    # Prepare data
    model = TrialDropoutModel()
    X = model.prepare_data(df)
    y = df['dropout'].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print('Training ensemble model (Random Forest + XGBoost)...')
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
        'patient_age': 45,
        'trial_duration': 12,
        'previous_participation': 1,
        'side_effects_severity': 6,
        'health_score': 70,
        'visit_compliance': 75
    }
    prediction = model.predict_dropout_risk(test_features)
    print(f'Trial Dropout Risk Prediction: {prediction}')


if __name__ == '__main__':
    train_trial_model()
