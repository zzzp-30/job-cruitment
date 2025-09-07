import type { BasePaginationResult } from './base';

export interface CompanyManager {
  uid: string;
  email: string;
  password?: string;
  first_name: string;
  last_name: string;
  data_join: string;
}

export interface Company {
  id: string;
  name: string;
  website: string;
  user: CompanyManager;
}

export interface CompanyListResponse extends BasePaginationResult {
  results: Company[];
}