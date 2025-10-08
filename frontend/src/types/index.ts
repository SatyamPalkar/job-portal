export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  target_roles?: string;
  industries?: string;
  experience_years?: number;
  created_at: string;
}

export interface Resume {
  id: number;
  user_id: number;
  title: string;
  is_original: boolean;
  content: string;
  raw_text?: string;
  summary?: string;
  keywords?: string;
  action_words?: string;
  created_at: string;
  updated_at: string;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  location?: string;
  job_type?: string;
  experience_level?: string;
  description: string;
  requirements?: string;
  responsibilities?: string;
  source: string;
  source_url?: string;
  keywords?: string;
  required_skills?: string;
  preferred_skills?: string;
  salary_range?: string;
  posted_date?: string;
  is_active: boolean;
  created_at: string;
}

export interface Application {
  id: number;
  user_id: number;
  job_id: number;
  resume_id: number;
  status: string;
  match_score?: number;
  optimizations_applied?: string;
  suggested_improvements?: string;
  cover_letter?: string;
  notes?: string;
  created_at: string;
  applied_at?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface JobSearchRequest {
  keywords?: string;
  location?: string;
  job_type?: string;
  experience_level?: string;
  limit?: number;
}

export interface ResumeOptimizeRequest {
  resume_id: number;
  job_id: number;
  optimization_level?: 'conservative' | 'balanced' | 'aggressive';
}

export interface ResumeOptimizeResponse {
  optimized_resume_id: number;
  match_score: number;
  optimizations_applied: string[];
  suggested_improvements: string[];
  optimized_content: string;
}


