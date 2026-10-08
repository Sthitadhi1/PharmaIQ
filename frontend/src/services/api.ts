import axios, { AxiosError } from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
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

export type ApiResult = {
  request: { method: string; url: string; body?: unknown };
  status: number;
  ok: boolean;
  data: any;
};

// For the test forms: never throws, so the HTTP status (200, 401, 422, ...) can be shown as-is.
export const callApi = async (
  method: 'get' | 'post',
  url: string,
  body?: unknown,
  headers?: Record<string, string>
): Promise<ApiResult> => {
  const request = { method: method.toUpperCase(), url: `/api${url}`, body };
  try {
    const response = await api.request({ method, url, data: body, headers, validateStatus: () => true });
    return { request, status: response.status, ok: response.status >= 200 && response.status < 300, data: response.data };
  } catch {
    return {
      request,
      status: 0,
      ok: false,
      data: { detail: 'Cannot reach the API. Is the backend running on port 8000?' }
    };
  }
};

export const apiRoot = (api.defaults.baseURL ?? '').replace(/\/api\/?$/, '');

// Turns any rejection from this module (FastAPI error body, Axios error or plain string)
// into a message that can be shown to the user.
export const getErrorMessage = (error: unknown, fallback: string): string => {
  const body = error instanceof AxiosError ? error.response?.data : error;
  if (typeof body === 'string' && body) return body;
  const detail = (body as { detail?: unknown } | undefined)?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail) && detail[0]?.msg) return String(detail[0].msg);
  return fallback;
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
