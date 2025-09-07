export interface ResumeResponse {
  id: string;
  name: string;
  user: string;
  url: string;
}
export interface Job {
  id: string;
  title: string;
  city: string;
  location: string;
  salary_min: number;
  salary_max: number;
  salary_count: number;
  experience: string;
  education: string;
  benefit: string;
  publish_time: string;
  company_name: string;
  company_avatar: string;
  company_tags: string;
  company_id: string;
}

import type { BasePaginationResult } from "./base";

export interface JobListResponse extends BasePaginationResult {
  results: Job[];
}
export interface JobDetailResponse extends Job {
  status: number;
  description: string;
  applied: boolean;
  company_size: string;
  company_website: string;
  has_resume: boolean;
}