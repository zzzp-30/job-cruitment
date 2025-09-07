export interface JobCreate {
  title: string;    // 职位名称
  status: number;    // 职位状态
  city: string;    // 职位所在城市
  location: string;    // 职位具体地址
  salary_min: number;    // 月薪最小值
  salary_max: number;    // 月薪最大值
  salary_count: number;    // 职位一年几薪
  hire_number: number;    // 计划招聘人数
  experience: string;    // 职位经验要求
  benefit: string;    // 职位福利
  description: string;    // 职位具体描述
  education: string;    // 职位学历要求
}
import type { BasePaginationResult } from "./base";

export interface Job extends JobCreate {
  id: string;
  pass_number: number;
  publish_time: string;
  resumes: number;
}

export interface ResponseJobList extends BasePaginationResult {
  results: Job[];
}