import type { AxiosResponse } from 'axios';
import { axiosInstance } from '../Axios';
import type{ LocationQuery } from 'vue-router';
import type { JobListResponse, ResumeResponse } from '../../types/Job';

const uploadResume = (file: File): Promise<AxiosResponse<ResumeResponse>> => {
  const form = new FormData();
  form.append('resume', file);
  return axiosInstance.post(`/resume/upload/`, form, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// 职位列表接口
const getJobList = (
  limit: number,
  offset: number,
  params: LocationQuery
): Promise<AxiosResponse<JobListResponse>> => {
  return axiosInstance.get('/job/', {
    params: {
      limit,
      offset,
      ...params,
    },
  });
};

import type { JobDetailResponse } from '../../types/Job';

// 职位详情接口
const getJobDetail = (
  id: string
): Promise<AxiosResponse<JobDetailResponse>> => {
  return axiosInstance.get(`/job/${id}/`);
};

// 申请面试接口
const applyJob = (jobId: string): Promise<AxiosResponse<null>> => {
  return axiosInstance.post(`/job/${jobId}/apply/`);
};

// 更新面试邀请消息接口
const replyInvitation = (
  iid: string,
  value: number
): Promise<AxiosResponse<null>> => {
  const updateData = {
    response: value,
  };
  return axiosInstance.patch(`/invitation/${iid}/`, updateData);
};

export { uploadResume, getJobList, getJobDetail, applyJob, replyInvitation };