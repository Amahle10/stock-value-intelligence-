import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 15000,
});

export const fetchPairs = () => api.get('/market/pairs');
export const fetchLatest = (pair: string) => api.get(`/market/latest/${pair}`);
export const fetchSummary = (pair: string) => api.get(`/analytics/summary/${pair}`);
export const fetchTimeAnalysis = (pair: string, metric = 'average_return') => api.get(`/analytics/time/${pair}`, { params: { metric } });
export const fetchReversal = (pair: string, horizon = '4h') => api.get(`/analytics/reversal/${pair}`, { params: { horizon } });
export const fetchModelPrediction = (pair: string) => api.get(`/models/prediction/${pair}`);
