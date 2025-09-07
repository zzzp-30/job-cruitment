import axios, {
  AxiosError,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from 'axios';
import { ElMessage } from 'element-plus';
import userStore from '../store/modules/User';

const UNAUTH_401 = '401: UnAuth';

const axiosConfig: AxiosRequestConfig = {
  baseURL: 'http://localhost:8080/api/', // api的base URL
  timeout: 10000, // 设置请求超时时间
  responseType: 'json',
  headers: {
    'Content-Type': 'application/json;charset=utf-8', // 传输数据类型
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
      ElMessage.error('登录状态已过期，请重新登录！');
      return Promise.reject(Error(UNAUTH_401));
    }
    return Promise.reject(error);
  }
);

export { axiosInstance, axiosConfig, UNAUTH_401 };