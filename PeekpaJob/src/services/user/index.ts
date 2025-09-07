import type { AxiosResponse } from 'axios';
import { axiosInstance } from '../Axios';
import type { AvatarResponse, LoginResponse } from '../../types/User';
import type { UpdateForm } from '../../types/base';

// 登录接口
const signin = (
  email: string,
  password: string
): Promise<AxiosResponse<LoginResponse>> => {
  return axiosInstance.post('/auth/signin/', {
    email,
    password,
  });
};
// 注册用户
const signup = (form: UpdateForm): Promise<AxiosResponse<LoginResponse>> => {
  return axiosInstance.post('/auth/signup/', form);
};

// 更新用户信息
const updateUserInfo = (
  form: UpdateForm
): Promise<AxiosResponse<UserSetting>> => {
  const updateForm: UpdateForm = {};
  updateForm.details = {};
  const outDetail = ['gender', 'password'];
  Object.entries(form).forEach(([key, value]) => {
    if (key in outDetail) {
      Object.assign(updateForm, { [key]: value });  
    } else {
      Object.assign(updateForm.details, { [key]: value });
    }
  });
  return axiosInstance.patch('/profile/', updateForm);
};
// 头像上传接口
const uploadAvatar = (file: File): Promise<AxiosResponse<AvatarResponse>> => {
  const form = new FormData();
  form.append('avatar', file);
  return axiosInstance.post(`/avatar/upload/`, form, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// 用户登出
const userLogout = (): Promise<AxiosResponse<null>> => {
  return axiosInstance.post('/auth/logout/');
};

import type { UserSetting } from '../../types/User';

// 请求个人信息
const getUserInfo = (): Promise<AxiosResponse<UserSetting>> => {
  return axiosInstance.get('/profile/');
};

export { signin, signup, updateUserInfo, uploadAvatar, userLogout, getUserInfo };

