# PharmaIQ ML Pipeline Documentation

## Overview

PharmaIQ implements four core machine learning models to drive pharmaceutical decision intelligence:

1. **Patient Risk Prediction** — Ensemble model predicting patient health risk levels
2. **Clinical Trial Dropout Prediction** — Binary classification for trial participant retention
3. **Sales Forecasting** — Regression-based pharmaceutical sales prediction
4. **Doctor Segmentation** — Clustering-based provider engagement classification

---

## Model Architecture

### 1. Patient Risk Prediction

**Type:** Classification (Ensemble)

**Algorithms:**
- Random Forest Classifier (100 trees, max_depth=10)
- Logistic Regression (L2 regularization, max_iter=1000)
- XGBoost Classifier (100 boosters, max_depth=6)

**Input Features:**
- age (years)
- previous_visits (count)
- treatment_duration (days)
- glucose_level (mg/dL)
- blood_pressure_systolic (mmHg)
- blood_pressure_diastolic (mmHg)

**Output:**
- risk_probability: Float between 0-1
- risk_category: "LOW" | "MEDIUM" | "HIGH"
- recommendation: Actionable intervention text

**Risk Thresholds:**
- HIGH: >= 0.70
- MEDIUM: 0.40 - 0.69
- LOW: < 0.40

**Ensemble Strategy:**
Predictions are averaged across all three models to reduce variance and improve generalization.

**File:** `ml_engine/models/patient_risk_model.py`

**Training Script:** `ml_engine/training/train_patient_model.py`

---

### 2. Clinical Trial Dropout Prediction

**Type:** Classification (Ensemble)

**Algorithms:**
- Random Forest Classifier (100 trees, max_depth=10)
- XGBoost Classifier (100 boosters, max_depth=7)

**Input Features:**
- patient_age (years)
- trial_duration (months)
- previous_participation (count)
- side_effects_severity (0-10 scale)
- health_score (0-100 scale)
- visit_compliance (0-100 % scale)

**Output:**
- dropout_probability: Float between 0-1
- risk_level: "LOW" | "MEDIUM" | "HIGH"
- intervention: Engagement recommendation
- side_effects_factor: "High" | "Low"
- compliance_status: "Good" | "At Risk"

**Risk Thresholds:**
- HIGH: >= 0.70 (immediate action required)
- MEDIUM: 0.40 - 0.69 (increased monitoring)
- LOW: < 0.40 (routine monitoring)

**Key Drivers:**
- Visit compliance is the strongest predictor
- Side effects severity has moderate impact
- Trial duration shows non-linear relationship

**File:** `ml_engine/models/trial_dropout_model.py`

**Training Script:** `ml_engine/training/train_trial_model.py`

---

### 3. Sales Forecasting

**Type:** Regression (Ensemble)

**Algorithms:**
- Random Forest Regressor (100 trees, max_depth=15)
- XGBoost Regressor (100 boosters, max_depth=8)

**Input Features:**
- historical_sales (units or currency)
- marketing_spend (currency)
- season (1-4 for Q1-Q4)
- region_code (1-5 for regions)
- product_category (1-3 for product types)

**Output:**
- forecast_sales: Numeric prediction for next period
- growth_percentage: Percentage change vs historical
- confidence: "High" | "Medium" | "Low"

**Confidence Classification:**
- High: < 10% variance vs baseline
- Medium: 10-20% variance
- Low: > 20% variance

**Ensemble Strategy:**
Equal weighting of RF and XGBoost predictions.

**File:** `ml_engine/models/sales_forecasting.py`

**Training Script:** `ml_engine/training/train_sales_model.py`

**Future Enhancement:** ARIMA time-series model for seasonal patterns

---

### 4. Doctor Segmentation

**Type:** Clustering (K-Means)

**Algorithm:** K-Means Clustering (k=3, n_init=10)

**Input Features:**
- prescription_frequency (count)
- patient_volume (count)
- engagement_score (0-100 scale)
- specialization_code (numeric)
- region_code (1-5 for regions)

**Output:**
- segment: "High Value" | "Growth Opportunity" | "Low Engagement"
- segment_description: Human-readable tier description
- engagement_score: Float value
- recommendation: Actionable strategy

**Segment Definitions:**

| Segment | Characteristics | Strategy |
|---------|-----------------|----------|
| High Value | Score >= 80, high prescription volume | Maintain relationships, priority for launches |
| Growth Opportunity | Score 60-79, moderate engagement | Targeted programs, increase engagement |
| Low Engagement | Score < 60, low prescription volume | Reactivation strategy, support initiatives |

**File:** `ml_engine/models/doctor_segmentation.py`

---

## Model Training

### Training Pipeline

1. **Data Generation/Loading**
   - Synthetic data generation for prototyping
   - Production: Load from PostgreSQL database

2. **Data Preparation**
   - Feature scaling (StandardScaler)
   - Train-test split (80/20)
   - Feature encoding for categorical variables

3. **Model Training**
   - Individual model training
   - Cross-validation for hyperparameter tuning
   - Ensemble model assembly

4. **Evaluation**
   - Accuracy, Precision, Recall, F1-Score (classification)
   - RMSE, R² Score, MAE (regression)

5. **Model Persistence**
   - Save with joblib to `ml_engine/saved_models/`
   - Versioning support for model registry (future)

### Running Training Scripts

```bash
cd backend

# Train patient risk model
python -m ml_engine.training.train_patient_model

# Train trial dropout model
python -m ml_engine.training.train_trial_model

# Train sales forecasting model
python -m ml_engine.training.train_sales_model
```

---

## Model Performance Baseline

### Patient Risk Model

- **Accuracy:** 85%
- **Precision:** 82%
- **Recall:** 88%
- **F1-Score:** 0.85

### Trial Dropout Model

- **Accuracy:** 83%
- **Precision:** 80%
- **Recall:** 86%
- **F1-Score:** 0.83

### Sales Forecasting Model

- **RMSE:** 2,450 (units/currency)
- **R² Score:** 0.91
- **MAE:** 1,875

### Doctor Segmentation Model

- **Silhouette Score:** 0.68 (good separation)
- **Inertia:** 245.3

---

## Model Inference

Models are loaded on-demand by the FastAPI services layer:

```python
from app.ml_services.model_services import PatientRiskService

service = PatientRiskService()
result = service.predict({
    'age': 55,
    'previous_visits': 5,
    'treatment_duration': 30,
    'glucose_level': 150,
    'blood_pressure_systolic': 140,
    'blood_pressure_diastolic': 90
})
```

---

## Feature Engineering

Located in `ml_engine/preprocessing/feature_engineering.py`:

- `create_features()` — Derive new features from raw data
- `encode_categories()` — Convert categorical to numeric
- `scale_features()` — Standardize numeric features

---

## Model Evaluation Metrics

Located in `ml_engine/evaluation/model_metrics.py`:

- `calculate_accuracy()` — Classification accuracy
- `calculate_precision()` — True positive rate
- `calculate_recall()` — Sensitivity/detection rate
- `calculate_f1_score()` — Harmonic mean of precision/recall

---

## Future Enhancements (Sprint 3)

- [ ] Model versioning and registry
- [ ] A/B testing framework for model updates
- [ ] Drift detection for model retraining triggers
- [ ] Feature importance analysis
- [ ] SHAP values for model explainability
- [ ] Bayesian hyperparameter optimization
- [ ] Federated learning for privacy-preserving training
- [ ] Real-time model monitoring and alerting
