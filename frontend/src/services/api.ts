import axios from 'axios';
import type {
  User,
  Resume,
  Job,
  Application,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  JobSearchRequest,
  ResumeOptimizeRequest,
  ResumeOptimizeResponse,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },
};

// Resume API
export const resumeApi = {
  getAll: async (): Promise<Resume[]> => {
    const response = await api.get<Resume[]>('/resumes/');
    return response.data;
  },

  getById: async (id: number): Promise<Resume> => {
    const response = await api.get<Resume>(`/resumes/${id}`);
    return response.data;
  },

  create: async (data: { title: string; content: string; is_original?: boolean }): Promise<Resume> => {
    const response = await api.post<Resume>('/resumes/', data);
    return response.data;
  },

  upload: async (file: File, title: string, isOriginal: boolean = true): Promise<Resume> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('is_original', String(isOriginal));

    const response = await api.post<Resume>('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  optimize: async (data: ResumeOptimizeRequest): Promise<ResumeOptimizeResponse> => {
    const response = await api.post<ResumeOptimizeResponse>('/resumes/optimize', data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/resumes/${id}`);
  },
};

// Job API
export const jobApi = {
  search: async (params: JobSearchRequest): Promise<Job[]> => {
    const response = await api.post<Job[]>('/jobs/search', params);
    return response.data;
  },

  getAll: async (params?: { skip?: number; limit?: number; keywords?: string; location?: string }): Promise<Job[]> => {
    const response = await api.get<Job[]>('/jobs/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Job> => {
    const response = await api.get<Job>(`/jobs/${id}`);
    return response.data;
  },

  getAnalysis: async (id: number): Promise<any> => {
    const response = await api.get(`/jobs/${id}/analysis`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/jobs/${id}`);
  },
};

// Application API
export const applicationApi = {
  getAll: async (): Promise<Application[]> => {
    const response = await api.get<Application[]>('/applications/');
    return response.data;
  },

  getById: async (id: number): Promise<Application> => {
    const response = await api.get<Application>(`/applications/${id}`);
    return response.data;
  },

  create: async (data: { job_id: number; resume_id: number; notes?: string }): Promise<Application> => {
    const response = await api.post<Application>('/applications/', data);
    return response.data;
  },

  update: async (id: number, data: { status?: string; notes?: string; cover_letter?: string }): Promise<Application> => {
    const response = await api.patch<Application>(`/applications/${id}`, data);
    return response.data;
  },

  generateCoverLetter: async (id: number): Promise<{ application_id: number; cover_letter: string }> => {
    const response = await api.post(`/applications/${id}/generate-cover-letter`);
    return response.data;
  },

  downloadResume: async (id: number, format: 'pdf' | 'docx' | 'txt'): Promise<any> => {
    const response = await api.get(`/applications/${id}/download/${format}`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/applications/${id}`);
  },
};

export default api;


