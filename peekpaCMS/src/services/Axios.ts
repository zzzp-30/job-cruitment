import axios, {
   AxiosError,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from 'axios';


const axiosConfig: AxiosRequestConfig = {
  baseURL: 'http://localhost:8080/api', // ✅ 正确：走 Nginx，且带 /api 前缀
  timeout: 10000,
  responseType: 'json',
  headers: {
    'Content-Type': 'application/json;charset=utf-8',
  },
};

// 创建axios实例
const axiosInstance = axios.create(axiosConfig);

axiosInstance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const newConfig = config;
  const store = userStore();
  newConfig.headers.authorization = `Bearer ${store.getToken}`;
  return newConfig;
});

import { ElMessage } from 'element-plus';
import router from '../route/index';
import ROUTER_CONSTANTS from '../route/constants';
import userStore from '../store/modules/User';

const UNAUTH_401 = '401: UnAuth';

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (
      error instanceof AxiosError &&
      error.response?.status === 401 &&
      error.response.data.code === 'user_inactive'
    ) {
      const store = userStore();
      store.logout();
      router.replace({
        name: ROUTER_CONSTANTS.LOGIN,
      });
      ElMessage.error('您的身份已经过期');
      return Promise.reject(Error(UNAUTH_401));
    }
    if (
      error instanceof AxiosError &&
      error.response?.status === 401 &&
      error.response.data.code === 'token_not_valid'
    ) {
      const store = userStore();
      store.logout();
      router.replace({
        name: ROUTER_CONSTANTS.LOGIN,
      });
      ElMessage.error('登录状态已过期，请重新登录！');
      return Promise.reject(Error(UNAUTH_401));
    }
    return Promise.reject(error);
  }
);

export { axiosInstance, axiosConfig, UNAUTH_401 };

