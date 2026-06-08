import axios, { AxiosError } from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

const handleError = (error: AxiosError) => {
  if (error.response) {
    return Promise.reject(error.response.data);
  }
  return Promise.reject(error.message);
};

export const getPatients = () => api.get('/patients').catch(handleError);
export const predictPatientRisk = (payload: object) => api.post('/ml/patient-risk', payload).catch(handleError);
export const getClinicalTrials = () => api.get('/trials').catch(handleError);
export const predictDropout = (payload: object) => api.post('/ml/trial-dropout', payload).catch(handleError);
export const getSales = () => api.get('/sales').catch(handleError);
export const forecastSales = (payload: object) => api.post('/ml/sales-forecast', payload).catch(handleError);
export const getDoctors = () => api.get('/doctors').catch(handleError);
export const segmentDoctors = (payload: object) => api.post('/ml/doctor-segment', payload).catch(handleError);
export const uploadAiDocument = (formData: FormData) =>
  api.post('/ai/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }).catch(handleError);
export const queryAiAssistant = (payload: object) => api.post('/ai/query', payload).catch(handleError);

export default api;
