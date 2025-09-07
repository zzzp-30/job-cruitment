<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { ElMessage, type FormInstance } from 'element-plus';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import useStore from '../../store/modules/User';
import ROUTER_CONSTANTS from '../../route/constants';
import { signin } from '../../services/user';

// 路由对象
const route = useRoute();
// 全局路由
const router = useRouter();
// 用户状态管理
const userStore = useStore();

interface LoginForm {
  email: string;
  password: string;
}

const param = reactive<LoginForm>({
  email: '',
  password: '',
});

// 登录表单引用
const ruleFormRef = ref<FormInstance>();

// 表单验证
const rules = computed(() => {
  return {
    email: [
      {
        required: true,
        message: '请输入用户名',
        trigger: 'blur',
      },
    ],
    password: [
      {
        required: true,
        message: '请输入密码',
        trigger: 'blur',
      },
    ],
  };
});

// 第一次进入页面，检测是否已经登录
onMounted(async () => {
  if (userStore.isLogin()) {
    await router.push({
      name: ROUTER_CONSTANTS.PROFILE,
    });
  }
});

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        const response = await signin(param.email, param.password);
        if (response.status === 200) {
          const userInfo = response.data;
          // 保存用户信息
          userStore.login(userInfo);
          ElMessage.success('登录成功');
          if (route.query.next) {
            router.replace(route.query.next as string);
          } else {
            // 默认跳转到首页
            router.replace({
              name: ROUTER_CONSTANTS.INDEX,
            });
          }
        }
      } catch (error) {
        ElMessage.error(`操作发生错误[${(error as AxiosError).message}]`);
      }
    } else {
      ElMessage.error('登录失败');
    }
  });
};
</script>

<template>
  <div class="login_container">
    <div class="login_main">
      <div class="title_main">
        <div class="title">欢迎登录 PeekpaJob</div>
      </div>
      <el-form
        ref="ruleFormRef"
        :model="param"
        :rules="rules"
        label-width="0px"
        size="large"
        class="ms-content"
      >
        <el-form-item prop="email">
          <el-input v-model="param.email" placeholder="请输入email"> </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="param.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            @keyup.enter="submitForm(ruleFormRef)"
          >
          </el-input>
        </el-form-item>
        <el-form-item>
          还没有账号？<a href="#/signup" class="register">点击注册</a>
        </el-form-item>
        <div class="login_btn">
          <el-button
            color="var(--theme-primary-color)"
            size="large"
            @click="submitForm(ruleFormRef)"
            >登录</el-button
          >
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.title_main {
  width: 100%;
  text-align: center;
  margin-bottom: 20px;
}
.title {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--theme-primary-color);
}
.login_container {
  height: calc(100vh - 170px - 60px - 40px);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.el-input {
  --el-input-focus-border-color: var(--theme-primary-color);
}
.login_main {
  width: 300px;
  margin: 0 auto;
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
  padding: 20px;
}

.login_btn {
  text-align: center;
}
.login_btn button {
  width: 100%;
  margin-bottom: 10px;
}

.register {
  color: var(--theme-primary-color);
  cursor: pointer;
  padding-left: 5px;
}
</style>