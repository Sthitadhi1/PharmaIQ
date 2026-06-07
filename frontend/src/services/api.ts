import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const getPatients = () => api.get('/patients');
export const predictPatientRisk = (payload: object) => api.post('/predict/patient-risk', payload);
export const getClinicalTrials = () => api.get('/clinical-trials');
export const predictDropout = (payload: object) => api.post('/predict/dropout', payload);
export const getSales = () => api.get('/sales');
export const forecastSales = (payload: object) => api.post('/forecast/sales', payload);
export const getDoctors = () => api.get('/doctors');
export const segmentDoctors = (payload: object) => api.post('/segment/doctors', payload);

export default api;
