import axios from 'axios';
import { AnalysisRecord, HistoryItem } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

export const apiService = {
  // Guest Session
  createGuestSession: async () => {
    const res = await apiClient.post('/auth/guest');
    return res.data;
  },

  // Upload & Process Image
  processImage: async (fileUri: string, anatomicalSite: string = 'Unspecified', token?: string): Promise<AnalysisRecord> => {
    const formData = new FormData();
    formData.append('anatomical_site', anatomicalSite);
    
    // In React Native / Web FormData
    const filename = fileUri.split('/').pop() || 'capture.jpg';
    const match = /\.(\w+)$/.exec(filename);
    const type = match ? `image/${match[1]}` : 'image/jpeg';

    formData.append('file', {
      uri: fileUri,
      name: filename,
      type,
    } as any);

    const headers: Record<string, string> = {
      'Content-Type': 'multipart/form-data',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await apiClient.post<AnalysisRecord>('/analysis/process', formData, { headers });
    return res.data;
  },

  // History
  getHistory: async (token?: string): Promise<HistoryItem[]> => {
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    const res = await apiClient.get<HistoryItem[]>('/analysis/history', { headers });
    return res.data;
  },

  // Delete Analysis
  deleteAnalysis: async (analysisId: string, token?: string): Promise<void> => {
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    await apiClient.delete(`/analysis/${analysisId}`, { headers });
  },

  // Education Articles
  getArticles: async () => {
    const res = await apiClient.get('/education/articles');
    return res.data;
  },
};
