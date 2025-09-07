<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import useStore from '../store/modules/User';
import { userLogout } from '../services/user';
import ROUTER_CONSTANTS from '../route/constants';

// User store
const userStore = useStore();

// 用户名下拉菜单选择事件
// 全局路由
const router = useRouter();

// 用户名下拉菜单选择事件
const handleCommand = async (command: string) => {
  if (command === 'loginout') {
    try {
      await userLogout();
      userStore.logout();
      await router.push({
        name: ROUTER_CONSTANTS.LOGIN,
      });
      ElMessage.success('登出成功');
    } catch (error) {
      ElMessage.error('登出失败');
      userStore.logout();
    }
  } else if (command === 'setting') {
    try {
      router.push({
        name: ROUTER_CONSTANTS.CMS_SETTING,
      });
    } catch (error) {
      ElMessage.error('发生错误');
    }
  }
};
const isSuperUser = () => {
  return userStore.getUser?.is_superuser;
};

</script>
<template>
  <div class="header">
    <a href="/" class="logo"></a>
    <div class="header_right">
      <div class="header_user_con">
        <el-dropdown class="user_name" trigger="click" @command="handleCommand">
          <span class="el-dropdown-link">
            <span v-if="isSuperUser()" class="name">超级管理员</span>
            <span v-else class="name">
              {{ userStore.getUser?.name }}
            </span>
            <el-icon><eli-CaretBottom /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-if="!isSuperUser()" command="setting"
                >修改资料</el-dropdown-item
              >
              <el-dropdown-item command="loginout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 1rem;
  background-color: var(--theme-one-color);
  display: flex;
  justify-content: space-between;
}
.header .logo {
  text-decoration: none;
  margin: auto 0;
  margin-left: 20px;
  width: 135px;
  height: 40px;
  background-image: url('../assets/logo-w.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
}
.header_right {
  float: right;
  padding-right: 50px;
}
.header_user_con {
  display: flex;
  height: 70px;
  align-items: center;
}
.user_name {
  margin-left: 10px;
  color: white;
}

.name {
  margin-right: 10px;
}

.el_dropdown_link {
  color: #fff;
  cursor: pointer;
}
.el_dropdown_menu__item {
  text-align: center;
}
</style>