# PharmaIQ API Documentation

## Base URL

`http://localhost:8000`

## Startup Endpoint

### GET `/`

Response:

```json
{
  "message": "PharmaIQ Life Sciences Intelligence API Running"
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

## Doctor Analytics Routes

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
