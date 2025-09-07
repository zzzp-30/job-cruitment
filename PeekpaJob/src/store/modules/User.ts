import { defineStore } from 'pinia';
import jwt_decode from 'jwt-decode';
import type { LoginResponse } from '../../types/User';
import type { UserAuthorizeInfo } from '../../types/User';

const PEEKPA_USER = 'PeekpaJob';

interface AuthToken {
  token: string;
}

// 定义 User Store
const userStore = defineStore('User', {
  // state 定义
  state: (): AuthToken => {
    return { token: localStorage.getItem(PEEKPA_USER) || '' };
  },
  getters: {
    // 获取用户
    getUser(auth: AuthToken): UserAuthorizeInfo | null {
      if (auth.token === '') {
        return null;
      }
      const userData = jwt_decode(auth.token) as UserAuthorizeInfo;
      return userData;
    },
    // 获取用户 JWT 令牌
    getToken(auth: AuthToken): string {
      return auth.token;
    },
  },
  actions: {
    // 判断是否有用户登录信息
    isLogin(): boolean {
      if (this.token === '') {
        return false;
      }
      const parsed = jwt_decode(this.token) as UserAuthorizeInfo;
      return parsed.exp > new Date().getTime() / 1000;
    },
    // 存储/更新用户信息
    login(auth: LoginResponse): void {
      this.token = auth.token;
      localStorage.setItem(PEEKPA_USER, auth.token);
    },
    // 登出
    logout() {
      localStorage.removeItem(PEEKPA_USER);
      this.token = '';
    },
  },
});



export default userStore;

