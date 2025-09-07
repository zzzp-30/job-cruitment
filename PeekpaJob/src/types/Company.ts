import type { BasePaginationResult } from "./base";

export interface Company {
  id: string;
  name: string;
  slogan: string;
  avatar: string;
  tags: string;
  size: string;
  jobs: number;
  interviews: number;
}
export interface CompanyListResponse extends BasePaginationResult {
  results: Company[];
}
import type { Job } from "./Job";

export interface CompanyDetailResponse {
  id: string;
  name: string;
  slogan: string;
  avatar: string;
  tags: string;
  size: string;
  jobs: Job[];
  website: string;
  description: string;
}