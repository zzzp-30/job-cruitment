import type { AxiosResponse } from 'axios';
import { axiosInstance } from '../Axios';
import type { Interview, JobNameItem, ResponseInterviewList } from '../../types/Interview';
import type { UpdateForm } from '../../types/base';
// 职位名称接口
const getAllJobName = (): Promise<AxiosResponse<JobNameItem[]>> => {
  return axiosInstance.get('/manage/job/list/');
};


// 面试列表接口
const getAllInterviews = (
  id: string,
  limit: number,
  offset: number
): Promise<AxiosResponse<ResponseInterviewList>> => {
  return axiosInstance.get(`/manage/job/${id}/interviews/`, {
    params: {
      limit,
      offset,
    },
  });
};

// 面试列表搜索接口
const searchInterview = (
  q: string,
  id: string,
  limit: number,
  offset: number
): Promise<AxiosResponse<ResponseInterviewList>> => {
  return axiosInstance.get(`/manage/job/${id}/interviews/`, {
    params: {
      q,
      limit,
      offset,
    },
  });
};
// 面试更新接口
const updateInterview = (
  id: string,
  iid: string,
  form: UpdateForm
): Promise<AxiosResponse<Interview>> => {
  return axiosInstance.patch(`/manage/job/${id}/interviews/${iid}/`, form);
};

const createInvitation = (
  id: string,
  iid: string,
  uid: string,
  message: string,
  status: number
): Promise<AxiosResponse<null>> => {
  return axiosInstance.post(`/manage/job/${id}/interviews/${iid}/invitation/`, {
    user_uid: uid,
    message,
    status,
  });
};

export { getAllJobName, getAllInterviews, searchInterview, updateInterview, createInvitation };