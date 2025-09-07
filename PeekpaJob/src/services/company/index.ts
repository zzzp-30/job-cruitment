import type { AxiosResponse } from 'axios';
import type { LocationQuery } from 'vue-router';
import { axiosInstance } from '../Axios';
import type {
  CompanyDetailResponse,
  CompanyListResponse,
} from '../../types/Company';

// 公司列表接口
const getCompanyList = (
  limit: number,
  offset: number,
  params: LocationQuery
): Promise<AxiosResponse<CompanyListResponse>> => {
  return axiosInstance.get('/company/', {
    params: {
      limit,
      offset,
      ...params,
    },
  });
};

// 公司详情接口
const getCompanyDetail = (
  id: string
): Promise<AxiosResponse<CompanyDetailResponse>> => {
  return axiosInstance.get(`/company/${id}/`);
};

export { getCompanyList, getCompanyDetail };