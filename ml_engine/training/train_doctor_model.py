import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from ml_engine.models.doctor_segmentation import DoctorSegmentationModel
from ml_engine.training.paths import SAVED_MODELS_DIR, save_metrics


def generate_sample_data(n_samples=300):
    """Generate synthetic doctor engagement data with three behavioural tiers."""
    np.random.seed(42)
    tier = np.random.choice([0, 1, 2], size=n_samples, p=[0.25, 0.4, 0.35])
    engagement_mean = np.array([88, 68, 40])[tier]
    data = {
        'prescription_frequency': np.clip(np.random.normal(np.array([120, 70, 25])[tier], 12), 0, None).round(),
        'patient_volume': np.clip(np.random.normal(np.array([400, 220, 90])[tier], 40), 0, None).round(),
        'engagement_score': np.clip(np.random.normal(engagement_mean, 6), 0, 100).round(1),
        'specialization_code': np.random.randint(1, 11, n_samples),
        'region_code': np.random.randint(1, 6, n_samples),
    }
    return pd.DataFrame(data)


def train_doctor_model(model_path: str = SAVED_MODELS_DIR):
    """Train and evaluate the doctor segmentation model."""
    print('=== Training Doctor Segmentation Model ===')

    df = generate_sample_data()
    print(f'Generated {len(df)} training samples')

    model = DoctorSegmentationModel(model_path=model_path)
    X = model.prepare_data(df)
    print('Training K-Means clustering (k=3)...')
    model.train(X)

    score = silhouette_score(X, model.kmeans_model.labels_)
    print(f'\nSilhouette Score: {score:.4f}')

    model.save_models()
    save_metrics('doctor_segmentation', {'silhouette': score, 'samples': len(df)}, model_path)
    print(f'\nModel saved to {model_path}')

    print('\n=== Sample Segmentation ===')
    test_features = {
        'prescription_frequency': 130,
        'patient_volume': 420,
        'engagement_score': 92,
        'specialization_code': 3,
        'region_code': 2
    }
    print(f'Doctor Segment: {model.segment_doctor(test_features)}')


main = train_doctor_model

if __name__ == '__main__':
    train_doctor_model()
