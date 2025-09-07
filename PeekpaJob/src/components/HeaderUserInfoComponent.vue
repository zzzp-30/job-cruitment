<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage } from 'element-plus';
import { computed } from 'vue';
import useStore from '../store/modules/User';
import { userLogout } from '../services/user';

// User Store
const userStore = useStore();

// username 计算属性，从User store中获取值
const username = computed(() => {
  const user = userStore.getUser;
  if (user) {
    return user.name;
  } else {
    return 'null';
  }
});

// 处理登出操作
const handleLogout = async () => {
  try {
    await userLogout();
    userStore.logout();
  } catch (error) {
    ElMessage.error(`登出失败[${(error as AxiosError).message}]`);
  }
};
</script>

<template>
  <ul v-if="userStore.isLogin()" class="account_bar">
    <li>
      <a href="/#/profile" class="username">{{ username }}</a>
    </li>
    <li>
      <a href="#" class="logout" @click.prevent="handleLogout">登出</a>
    </li>
  </ul>
  <ul v-else class="login_register">
    <li>
      <a href="/#/signin">登录</a>
    </li>
    <li>
      <span class="diver">|</span>
    </li>
    <li>
      <a href="/#/signup">注册</a>
    </li>
  </ul>
</template>

<style scoped>
.account_bar {
  list-style: none;
}

.account_bar li {
  position: relative;
  text-align: center;
  float: left;
}

.account_bar li a {
  display: inline-block;
  height: 40px;
  line-height: 60px;
  padding-left: 20px;
  text-decoration: none;
}

.login_register {
  list-style: none;
}

.login_register li {
  position: relative;
  text-align: center;
  float: left;
}
.diver {
  padding: 0 15px;
  color: #5e6166;
  line-height: 60px;
  text-align: center;
}

.login_register li a {
  display: inline-block;
  height: 60px;
  line-height: 60px;
  color: var(--theme-secondary-color);
  text-decoration: none;
  transition: color 0.3s;
}
.login_register a:hover {
  color: var(--theme-third-color);
}

.username {
  color: var(--theme-third-color);
  font-weight: bolder;
  font-size: 1.1rem;
}

.logout {
  color: var(--theme-secondary-color);
}
</style>