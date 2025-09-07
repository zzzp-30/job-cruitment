import type{ IndexResponse } from '../../types/Common';
import { axiosInstance } from '../Axios';
import type { AxiosResponse } from 'axios';

// 首页接口
const getIndexData = (): Promise<AxiosResponse<IndexResponse>> => {
  return axiosInstance.get(`/index/`);
};

export { getIndexData }