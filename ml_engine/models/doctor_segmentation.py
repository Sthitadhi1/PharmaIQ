import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os


class DoctorSegmentationModel:
    """
    Doctor Segmentation Model using K-Means clustering.
    Segments healthcare providers into 3 tiers based on engagement and behavior.
    """

    def __init__(self, model_path: str = 'ml_engine/saved_models/', n_clusters: int = 3):
        self.model_path = model_path
        self.kmeans_model = None
        self.scaler = StandardScaler()
        self.n_clusters = n_clusters
        self.feature_names = [
            'prescription_frequency', 'patient_volume', 'engagement_score', 'specialization_code', 'region_code'
        ]
        self.segment_labels = {
            0: {'name': 'High Value', 'description': 'Top tier doctors with strong engagement'},
            1: {'name': 'Growth Opportunity', 'description': 'Mid-tier with growth potential'},
            2: {'name': 'Low Engagement', 'description': 'Requires targeted outreach'}
        }

    def prepare_data(self, df: pd.DataFrame):
        """Prepare and scale data for clustering."""
        X = df[self.feature_names].values
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def train(self, X: np.ndarray):
        """Train K-Means clustering model."""
        self.kmeans_model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.kmeans_model.fit(X)

    def predict_segment(self, X: np.ndarray) -> np.ndarray:
        """
        Predict cluster segment for doctors.
        """
        if self.kmeans_model is None:
            raise ValueError('Model not trained. Call train() first or load_models().')

        return self.kmeans_model.predict(X)

    def segment_doctor(self, features: dict) -> dict:
        """
        Segment a doctor based on features.
        Returns segment classification and insights.
        """
        X = np.array([[
            features.get('prescription_frequency', 50),
            features.get('patient_volume', 100),
            features.get('engagement_score', 75),
            features.get('specialization_code', 1),
            features.get('region_code', 1)
        ]])

        X_scaled = self.scaler.transform(X)
        segment_id = self.predict_segment(X_scaled)[0]
        segment_info = self.segment_labels.get(segment_id, {'name': 'Unknown', 'description': 'Unclassified'})

        return {
            'segment': segment_info['name'],
            'segment_description': segment_info['description'],
            'engagement_score': round(float(features.get('engagement_score', 0)), 2),
            'recommendation': self._get_recommendation(segment_info['name'])
        }

    def _get_recommendation(self, segment_name: str) -> str:
        """Get actionable recommendation based on segment."""
        recommendations = {
            'High Value': 'Maintain relationship and prioritize for new product launches',
            'Growth Opportunity': 'Increase engagement through targeted programs',
            'Low Engagement': 'Implement reactivation strategy and support initiatives'
        }
        return recommendations.get(segment_name, 'Monitor performance')

    def save_models(self):
        """Save trained models to disk."""
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.kmeans_model, os.path.join(self.model_path, 'doctor_kmeans_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'doctor_scaler.pkl'))

    def load_models(self):
        """Load trained models from disk."""
        self.kmeans_model = joblib.load(os.path.join(self.model_path, 'doctor_kmeans_model.pkl'))
        self.scaler = joblib.load(os.path.join(self.model_path, 'doctor_scaler.pkl'))
