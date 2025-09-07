<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ROUTER_CONSTANTS from '../../route/constants';
import { login } from '../../services/user';
import useStore from '../../store/modules/User';

// 全局路由
const router = useRouter();
// User store
const userStore = useStore();
// 登录表单引用
const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
// 登录表单接口
interface LoginForm {
  email: string;
  password: string;
}

const param = reactive<LoginForm>({
  email: '',
  password: '',
});

// 表单验证
const rules = {
  email: [{ required: true, message: '请输入email', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
};

// 提交表单
// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  loading.value = true;
  await formEl.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await login(param.email, param.password);
        if (response.status === 200) {
          const { data } = response;
          // 保存用户信息
          userStore.login(data);
          // 默认跳转到首页
          loading.value = false;
          let result = null;
          if (userStore.getUser?.is_superuser) {
            result = await router.push({
              name: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
            });
          } else {
            result = await router.push({
              name: ROUTER_CONSTANTS.CMS_DASHBOARD,
            });
          }

          if (!result) {
            ElMessage.success('登录成功');
          }
        }
      } catch (error) {
        ElMessage.error(`登录失败[${(error as AxiosError).message}]`);
        loading.value = false;
      }
    } else {
      ElMessage.error('登录出错');
      loading.value = false;
    }
  });
};
// 第一次进入页面，判断用户是否已经登录，如果登录则跳转到首页
onMounted(() => {
  if (userStore.isLogin()) {
    if (userStore.getUser?.is_superuser) {
      router.push({
        name: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
      });
    } else {
      router.push({
        name: ROUTER_CONSTANTS.CMS_DASHBOARD,
      });
    }
  }
});
</script>
<template>
  <div class="login_wrap">
    <div class="ms_login">
      <div class="ms_title">Peekpa 管理系统</div>
      <el-form
        ref="ruleFormRef"
        :model="param"
        :rules="rules"
        label-width="0px"
        size="large"
        class="ms_content"
      >
        <el-form-item prop="username">
          <el-input v-model="param.email" placeholder="请输入邮箱">
            <template #prepend>
              <el-icon>
                <eli-user />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="param.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            @keyup.enter="submitForm(ruleFormRef)"
          >
            <template #prepend>
              <el-icon>
                <eli-lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <div class="login_btn">
          <el-button
            :loading="loading"
            type="primary"
            @click="submitForm(ruleFormRef)"
            >登录</el-button
          >
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.login_wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background: #324157;
  background: linear-gradient(to top, #ffffff, #4b5679);
  background-size: 100%;
}
.ms_title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 1.2rem;
  color: #ffffff;
  border-bottom: 1px solid #ddd;
  font-family: HyliaSerif;
}
.ms_login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms_content {
  padding: 30px 30px;
}
.login_btn {
  text-align: center;
}
.login_btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
</style>

