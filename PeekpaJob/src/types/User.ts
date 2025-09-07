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

export interface AvatarResponse {
  id: string;
  name: string;
  user: string;
  url: string;
}
// 用户详细信息
export interface UserDetails {
  phone: string;
  avatar: string;
  position: string;
  education: string;
  school: string;
  major: string;
  experience_year: string;
  status: string;
  city: string;
  company_name: string;
  salary_min: string;
  salary_max: string;
}

// 简历
export interface Resume {
  name: string;
  url: string;
}
// 面试邀请信息
export interface Invitation {
  id: string;
  response: number;
  publish_time: string;
  due_time: string;
  message: string;
  update_time: string;
}

// 面试职位
export interface UserApplication {
  id: string;
  title: string;
  status: number;
  salary_min: number;
  salary_max: number;
  salary_count: number;
  company_name: string;
  timestamp: string;
  invitation: Invitation;
}

// 用户个人信息
export interface UserSetting {
  email: string;
  first_name: string;
  last_name: string;
  gender: number;
  details: UserDetails;
  password?: string;
  resume: Resume;
  applications: UserApplication[];
}