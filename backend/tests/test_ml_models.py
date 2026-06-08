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
