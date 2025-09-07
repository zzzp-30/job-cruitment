// 用户store信息
export interface UserAuthorizeInfo {
  exp: number; // expire time
  iat: number; // issue at time
  uid: string; // 用户uid
  is_staff: boolean; // 用户权限
  is_manager: boolean; // 权限
  is_superuser?: boolean; // 权限
  email: string; // 用户email
  name: string; // 用户名
}
export interface LoginResponse {
  token: string;
}
import type { BasePaginationResult } from "./base";

export interface User {
  uid: string;
  email: string;
  first_name: string;
  last_name: string;
  gender: number;
  data_join: string;
  last_login: string;
  password?: string;
  is_active: boolean;
}

export interface UserListResponse extends BasePaginationResult {
  results: User[];
}

export interface UserSetting {
  avatar: string;
  name: string;
  description: string;
  size: string;
  slogan: string;
  tags: string | string[];
  website: string;
  user: {
    email: string;
    name: string;
    gender: number;
  };
  password?: string;
  avatar_file?: File;
}