# PharmaIQ API Documentation

## Base URL

`http://localhost:8000`

## Health Check

### GET `/health`

Response:

```json
{
  "status": "healthy",
  "environment": "development"
}
```

## Patient Routes

### GET `/api/patients`

Response:

```json
{
  "patients": []
}
```

### POST `/api/predict/patient-risk`

Request body:

```json
{
  "patient_id": 1001
}
```

Response:

```json
{
  "risk_score": 0,
  "category": "Pending ML Integration"
}
```

---

## ML Intelligence Endpoints (Sprint 2)

### POST `/api/ml/patient-risk`

Predict patient risk level using ensemble ML models (Random Forest, Logistic Regression, XGBoost).

Request body:

```json
{
  "age": 55,
  "previous_visits": 5,
  "treatment_duration": 30,
  "glucose_level": 150,
  "blood_pressure_systolic": 140,
  "blood_pressure_diastolic": 90
}
```

Response:

```json
{
  "risk_probability": 0.782,
  "risk_category": "HIGH",
  "recommendation": "Immediate medical attention recommended"
}
```

### POST `/api/ml/trial-dropout`

Predict probability of patient dropout from clinical trials.

Request body:

```json
{
  "patient_age": 45,
  "trial_duration": 12,
  "previous_participation": 1,
  "side_effects_severity": 6,
  "health_score": 70,
  "visit_compliance": 75
}
```

Response:

```json
{
  "dropout_probability": 0.642,
  "risk_level": "MEDIUM",
  "intervention": "Increased monitoring and support recommended",
  "side_effects_factor": "High",
  "compliance_status": "At Risk"
}
```

### POST `/api/ml/sales-forecast`

Forecast pharmaceutical sales using RF + XGBoost ensemble.

Request body:

```json
{
  "historical_sales": 50000,
  "marketing_spend": 15000,
  "season": 2,
  "region_code": 3,
  "product_category": 2
}
```

Response:

```json
{
  "forecast_sales": 58750.50,
  "growth_percentage": 17.5,
  "confidence": "High"
}
```

### POST `/api/ml/doctor-segment`

Segment healthcare provider into tiers using K-Means clustering.

Request body:

```json
{
  "prescription_frequency": 980,
  "patient_volume": 245,
  "engagement_score": 89.2,
  "specialization_code": 1,
  "region_code": 1
}
```

Response:

```json
{
  "segment": "High Value",
  "segment_description": "Top tier doctors with strong engagement",
  "engagement_score": 89.2,
  "recommendation": "Maintain relationship and prioritize for new product launches"
}
```

---

## Clinical Trial Routes

### GET `/api/trials`

Response:

```json
{
  "trials": []
}
```

### POST `/api/predict/trial-dropout`

Response:

```json
{
  "dropout_probability": 0,
  "status": "Model Integration Pending"
}
```

---

## Sales Routes

### GET `/api/sales`

Response:

```json
{
  "sales": []
}
```

### POST `/api/forecast/sales`

Response:

```json
{
  "forecast": "Future ML Forecasting Module"
}
```

---

## Doctor Routes

### GET `/api/doctors`

Response:

```json
{
  "doctors": []
}
```

### POST `/api/segment/doctors`

Response:

```json
{
  "segment": "KMeans Model Pending"
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` — Success
- `400` — Bad request
- `404` — Not found
- `500` — Server error

Error response format:

```json
{
  "detail": "Error description"
}
```

---

## Authentication (Coming Sprint 3)

- JWT token-based authentication
- Role-based access control (ADMIN, DATA_ANALYST, DOCTOR)
- Protected routes requiring authorization header

---

## Rate Limiting (Coming Sprint 3)

- Requests limited to 1000 per hour per IP
- Prediction endpoints: 100 per minute

---

## Versioning

Current API version: **v1**

Future versions will be accessible via:

- `/api/v2/...`
- `/api/v3/...`
