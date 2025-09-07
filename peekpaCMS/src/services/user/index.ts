import type { AxiosResponse } from "axios";
import { axiosInstance } from "../Axios";
import type { LoginResponse, UserListResponse } from "../../types/User";
import type { UpdateForm } from "../../types/base";
import type { UserSetting } from "../../types/User";
// login接口
const login = (
  email: string,
  password: string
): Promise<AxiosResponse<LoginResponse>> => {
  return axiosInstance.post('/auth/login/', {  // ✅ 改为 /login/，和后端一致
    email,
    password,
  });
};


// 用户登出
const userLogout = (): Promise<AxiosResponse<null>> => {
  return axiosInstance.post('/auth/logout/');
};




// 用户列表
const getAllUsers = (
  limit: number,
  offset: number
): Promise<AxiosResponse<UserListResponse>> => {
  return axiosInstance.get('/manage/user/', {
    params: {
      limit,
      offset,
    },
  });
};

// 用户搜索
const searchUser = (
  q: string,
  limit: number,
  offset: number
): Promise<AxiosResponse<UserListResponse>> => {
  return axiosInstance.get('/manage/user/', {
    params: {
      q,
      limit,
      offset,
    },
  });
};

// 更新用户
const updateUser = (
  uid: string,
  form: UpdateForm
): Promise<AxiosResponse<null>> => {
  return axiosInstance.patch(`/manage/user/${uid}/`, form);
};

// 新建用户
const createUser = (form: UpdateForm): Promise<AxiosResponse<null>> => {
  return axiosInstance.post(`/manage/user/`, form);
};

const getUserInfo = (): Promise<AxiosResponse<UserSetting>> => {
  return axiosInstance.get('/manage/setting/');
};

// 更新用户信息
const updateUserInfo = (form: FormData): Promise<AxiosResponse<null>> => {
  return axiosInstance.patch('/manage/setting/', form, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export {
  login,
  userLogout,
  getAllUsers,
  searchUser,
  updateUser,
  createUser,
  getUserInfo,
  updateUserInfo,
}