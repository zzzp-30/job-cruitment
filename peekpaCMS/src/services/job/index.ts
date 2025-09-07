import type { AxiosResponse } from 'axios';
import { axiosInstance } from '../Axios';
import type { Job, JobCreate, ResponseJobList } from '../../types/Job';
import type { UpdateForm } from '../../types/base';
const createJob = (form: JobCreate): Promise<AxiosResponse<null>> => {
  return axiosInstance.post('/manage/job/', {
    ...form,
  });
};

const getAllJobs = (
  limit: number,
  offset: number
): Promise<AxiosResponse<ResponseJobList>> => {
  return axiosInstance.get('/manage/job/', {
    params: {
      limit,
      offset,
    },
  });
};

const searchJob = (
  q: string,
  limit: number,
  offset: number
): Promise<AxiosResponse<ResponseJobList>> => {
  return axiosInstance.get('/manage/job/', {
    params: {
      q,
      limit,
      offset,
    },
  });
};

const updateJob = (
  id: string,
  form: UpdateForm
): Promise<AxiosResponse<Job>> => {
  return axiosInstance.patch(`/manage/job/${id}/`, form);
};
export { createJob, getAllJobs, searchJob, updateJob }