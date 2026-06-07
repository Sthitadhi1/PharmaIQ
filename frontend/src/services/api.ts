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
export const predictPatientRisk = (payload: object) => api.post('/predict/patient-risk', payload).catch(handleError);
export const getClinicalTrials = () => api.get('/trials').catch(handleError);
export const predictDropout = (payload: object) => api.post('/predict/trial-dropout', payload).catch(handleError);
export const getSales = () => api.get('/sales').catch(handleError);
export const forecastSales = (payload: object) => api.post('/forecast/sales', payload).catch(handleError);
export const getDoctors = () => api.get('/doctors').catch(handleError);
export const segmentDoctors = (payload: object) => api.post('/segment/doctors', payload).catch(handleError);

export default api;
