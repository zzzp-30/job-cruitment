import type { AxiosResponse } from 'axios';
import { axiosInstance } from '../Axios';
import type { DashboardResponse } from '../../types/Dashboard';

// 首页接口
const getDashboard = (): Promise<AxiosResponse<DashboardResponse>> => {
  return axiosInstance.get('/manage/dashboard/');
};

export default getDashboard;