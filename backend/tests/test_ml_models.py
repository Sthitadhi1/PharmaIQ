import pytest
import numpy as np


def test_patient_risk_model_import():
    from ml_engine.models.patient_risk_model import PatientRiskModel
    model = PatientRiskModel()
    assert model is not None


def test_trial_dropout_model_import():
    from ml_engine.models.trial_dropout_model import TrialDropoutModel
    model = TrialDropoutModel()
    assert model is not None


def test_sales_forecasting_model_import():
    from ml_engine.models.sales_forecasting import SalesForecastingModel
    model = SalesForecastingModel()
    assert model is not None


def test_doctor_segmentation_model_import():
    from ml_engine.models.doctor_segmentation import DoctorSegmentationModel
    model = DoctorSegmentationModel()
    assert model is not None


def test_training_package_imports():
    # BUG-02: ml_engine/training/__init__.py imported a non-existent `main`.
    from ml_engine.training import (
        train_doctor_model, train_patient_model, train_sales_model, train_trial_model
    )
    assert all(callable(fn) for fn in (train_doctor_model, train_patient_model, train_sales_model, train_trial_model))


def test_patient_training_labels_depend_on_features():
    # BUG-17: labels were np.random.randint, so the model could only learn noise.
    from ml_engine.training.train_patient_model import generate_sample_data
    df = generate_sample_data(n_samples=1000)
    older = df[df['age'] >= 65]['risk'].mean()
    younger = df[df['age'] < 35]['risk'].mean()
    assert older > younger + 0.2


def test_doctor_segments_follow_engagement(tmp_path):
    # BUG-18: K-Means cluster ids are arbitrary, so cluster 0 was not necessarily "High Value".
    from ml_engine.models.doctor_segmentation import DoctorSegmentationModel
    from ml_engine.training.train_doctor_model import generate_sample_data

    model = DoctorSegmentationModel(model_path=str(tmp_path))
    model.train(model.prepare_data(generate_sample_data()))
    model.save_models()

    reloaded = DoctorSegmentationModel(model_path=str(tmp_path))
    reloaded.load_models()
    high = reloaded.segment_doctor({'prescription_frequency': 130, 'patient_volume': 420,
                                    'engagement_score': 92, 'specialization_code': 3, 'region_code': 2})
    low = reloaded.segment_doctor({'prescription_frequency': 20, 'patient_volume': 80,
                                   'engagement_score': 35, 'specialization_code': 3, 'region_code': 2})
    assert high['segment'] == 'High Value'
    assert low['segment'] == 'Low Engagement'
