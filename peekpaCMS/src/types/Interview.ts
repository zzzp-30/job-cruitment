import type { BasePaginationResult } from "./base";

// 求职者信息
export interface InterviewCandidate {
  uid: string;
  name: string;
  gender: number;
  email: string;
  details: string;
}

// 面试职位
export interface InterviewJob {
  id: string;
  title: string;
  hire_number: number;
  pass_number: number;
}

// 面试的简历
export interface InterviewResume {
  name: string;
  url: string;
}

// 面试消息
export interface InterviewInvitation {
  id: string;
  response: number;
  message: string;
  due_time: string;
  publish_time: string;
  update_time: string;
}

export interface Interview {
  id: string;
  interviewer: string;
  status: number;
  feedback: JSON;
  candidate: InterviewCandidate;
  job: InterviewJob;
  resume: InterviewResume;
  invitation: InterviewInvitation | null;
  publish_time: string;
}

export interface ResponseInterviewList extends BasePaginationResult {
  results: Interview[];
}
export interface JobNameItem {
  id: string;
  title: string;
}