export interface DashboardItem {
  id: string;
  title: string;
  publish_time: string;
}

export interface DashboardResponse {
  jobs_open: number;
  jobs_total: number;
  jobs_finish: number;
  jobs_close: number;
  interviewing: number;
  resumes: number;
  resumes_new: number;
  hired_number: number;
  pass_number: number;
  users_number: number;
  invitation_number: number;
  new_jobs: DashboardItem[];
  new_interviews: DashboardItem[];
}