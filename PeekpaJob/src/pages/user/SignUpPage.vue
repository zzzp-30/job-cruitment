<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { type InternalRuleItem } from 'async-validator';
import ROUTER_CONSTANTS from '../../route/constants';
import { signup, updateUserInfo, uploadAvatar } from '../../services/user';
import useStore from '../../store/modules/User';
import { uploadResume } from '../../services/job';

// 路由对象
const route = useRoute();
// 全局路由
const router = useRouter();
// User store
const userStore = useStore();
// 注册步骤变量
const step = ref<number>(1);

interface LoginForm {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

const signupForm = reactive<LoginForm>({
  email: '',
  first_name: '',
  last_name: '',
  password: '',
});

// 注册信息表单引用
const ruleFormRef = ref<FormInstance>();

// 自定义验证规则，检测姓名
const validateName = (
  _rule: InternalRuleItem,
  _value: string,
  callback: (error?: string | Error) => void
) => {
  if (signupForm.first_name.length && signupForm.last_name.length) {
    callback();
  } else {
    callback(new Error('请正确输入姓名'));
  }
};

// 表单验证规则
const rules = computed(() => {
  return {
    email: [
      {
        required: true,
        message: '请输入邮箱',
        trigger: 'blur',
      },
    ],
    name: [
      {
        required: true,
        validator: validateName,
        trigger: 'submit',
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

onMounted(async () => {
  if (userStore.isLogin()) {
    await router.push({
      name: ROUTER_CONSTANTS.PROFILE,
    });
  }
});

// 提交注册信息表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        const response = await signup(signupForm);
        if (response.status === 201) {
          const userInfo = response.data;
          // 保存用户信息
          userStore.login(userInfo);
          formEl.resetFields();
          step.value = 2;
        }
      } catch (error) {
        ElMessage.error(`注册失败[${(error as AxiosError).message}]`);
      }
    } else {
      ElMessage.error('请检查表格内容');
    }
  });
};
const previewInput = ref<HTMLInputElement | null>(null);

const resumeInput = ref<HTMLInputElement | null>(null);

const selectedImage = ref<string>('');

const genderList = [
  {
    name: '请选择',
    value: 0,
  },
  {
    name: '男',
    value: 1,
  },
  {
    name: '女',
    value: 2,
  },
];

const experienceList = ['无经验', '2年以内', '2~5年', '5~10年', '10年以上'];

const statusList = ['目前状态', '在职', '已离职', '无业'];

const educationList = ['博士', '研究生', '大学', '高中', '初中', '初中以下'];

interface InfoForm {
  phone: string;
  gender: number;
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

// 详细信息表单
const infoForm = reactive<InfoForm>({
  phone: '',
  avatar: '',
  gender: 0,
  position: '',
  education: '',
  school: '',
  major: '',
  experience_year: '',
  status: '',
  city: '',
  company_name: '',
  salary_min: '',
  salary_max: '',
});

// 自定义验证用户性别
const validateGender = (
  _rule: InternalRuleItem,
  value: number,
  callback: (error?: string | Error) => void
) => {
  if (value !== 0) {
    callback();
  } else {
    callback(new Error('请选择性别'));
  }
};

// 详细信息的表单验证规则
const infoRules = computed(() => {
  return {
    phone: [
      {
        required: true,
        message: '请输入手机号码',
        trigger: 'blur',
      },
    ],
    gender: [
      {
        required: true,
        validator: validateGender,
        trigger: 'blur',
      },
    ],
    position: [
      {
        required: true,
        message: '请输入想要应聘的职位',
        trigger: 'blur',
      },
    ],
    experience_year: [
      {
        required: true,
        message: '请选择工作经验',
        trigger: 'blur',
      },
    ],
    status: [
      {
        required: true,
        message: '请输入目前的状态',
        trigger: 'blur',
      },
    ],
    education: [
      {
        required: true,
        message: '请填写最高学历',
        trigger: 'blur',
      },
    ],
    school: [
      {
        required: true,
        message: '请输入学校名称',
        trigger: 'blur',
      },
    ],
    city: [
      {
        required: true,
        message: '请输入城市',
        trigger: 'blur',
      },
    ],
  };
});

// 提交详细信息内容
const submitInfoForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        const response = await updateUserInfo(infoForm);
        if (response.status === 200) {
          formEl.resetFields();
          ElMessage.success('注册成功，正在跳转');
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
        ElMessage.error(`注册失败[${(error as AxiosError).message}]`);
      }
    } else {
      ElMessage.error('请检查表格内容');
    }
  });
};

const uploadPreview = () => {
  if (previewInput.value) {
    previewInput.value.click();
  }
};

// 上传头像
const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length) {
    const file = target.files[0];
    try {
      const response = await uploadAvatar(file);
      if (response.status === 201) {
        selectedImage.value = `${import.meta.env.VITE_COMPANY_SITE_URL}/${response.data.url}`;
        infoForm.avatar = selectedImage.value;
      } else {
        ElMessage.error(`头像上传失败[${response.status}]`);
      }
    } catch (error) {
      ElMessage.error(`头像上传失败[${(error as AxiosError).message}]`);
    }
  }
};

// 上传简历
const handleResumeChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length) {
    const file = target.files[0];
    try {
      const response = await uploadResume(file);
      if (response.status !== 201) {
        ElMessage.error(`上传失败[${response.status}]`);
      }
    } catch (error) {
      ElMessage.error(`上传失败[${(error as AxiosError).message}]`);
    }
  }
};
</script>

<template>
  <div class="register_container">
    <!-- 第一步：注册表单 -->
    <div v-if="step === 1" class="register_main">
      <div class="title_main">
        <div class="title">注册 PeekpaJob</div>
      </div>

      <el-form
        ref="ruleFormRef"
        :model="signupForm"
        :rules="rules"
        label-width="80px"
        size="large"
        class="ms-content"
      >
        <!-- 邮箱 -->
        <el-form-item prop="email" label="邮箱">
          <el-input v-model="signupForm.email" placeholder="请输入邮箱" />
        </el-form-item>

        <!-- 姓名：姓和名 -->
        <el-form-item prop="name" label="姓名">
          <el-col :span="11">
            <el-input v-model="signupForm.last_name" placeholder="姓" />
          </el-col>
          <el-col :span="11" :offset="2">
            <el-input v-model="signupForm.first_name" placeholder="名" />
          </el-col>
        </el-form-item>

        <!-- 密码 -->
        <el-form-item prop="password" label="密码">
          <el-input
            v-model="signupForm.password"
            placeholder="请输入密码"
            type="password"
          />
        </el-form-item>

        <!-- 注册按钮 -->
        <div class="register_btn">
          <el-button
            color="var(--theme-primary-color)"
            size="large"
            @click="submitForm(ruleFormRef)"
          >
            注册
          </el-button>
        </div>
      </el-form>
    </div>

    <!-- 第二步：补充信息 -->
    <div v-else-if="step === 2" class="info_main">
      <div class="title_main">
        <div class="title">注册成功，请补充以下材料</div>
      </div>

      <el-form
        ref="ruleFormRef"
        :model="infoForm"
        :rules="infoRules"
        label-width="80px"
        size="large"
        class="ms-content"
      >
        <el-row>
          <!-- 左侧信息栏 -->
          <el-col :span="16">
            <!-- 联系方式 + 性别 -->
            <el-row :gutter="10">
              <el-col :span="12">
                <el-form-item prop="phone" label="联系方式">
                  <el-input
                    v-model="infoForm.phone"
                    placeholder="请输入手机号码"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item prop="gender" label="性别">
                  <el-select
                    v-model="infoForm.gender"
                    default-first-option
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in genderList"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 应聘职位 + 目前状态 -->
            <el-row :gutter="10">
              <el-col :span="12">
                <el-form-item prop="position" label="应聘职位">
                  <el-input
                    v-model="infoForm.position"
                    placeholder="想要应聘的职位"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item prop="status" label="目前状态">
                  <el-select
                    v-model="infoForm.status"
                    default-first-option
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in statusList"
                      :key="item"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 工作经验 + 公司名称 -->
            <el-row :gutter="10">
              <el-col :span="12">
                <el-form-item prop="experience_year" label="工作经验">
                  <el-select
                    v-model="infoForm.experience_year"
                    default-first-option
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in experienceList"
                      :key="item"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="公司名称">
                  <el-input
                    v-model="infoForm.company_name"
                    placeholder="现公司名称"
                  />
                </el-form-item>
              </el-col>
            </el-row>
          </el-col>

          <!-- 右侧：头像上传 -->
          <el-col :span="8">
            <el-form-item label="头像">
              <input
                ref="previewInput"
                type="file"
                hidden
                accept=".png, .jpg, .jpeg"
                @change="handleFileChange"
              />
              <div class="preview" @click="uploadPreview">
                <el-image :src="selectedImage" fit="fill" class="image">
                  <template #error>
                    <div class="image-error" />
                  </template>
                  <template #placeholder>
                    <div class="image-slot">
                      Loading<span class="dot">...</span>
                    </div>
                  </template>
                </el-image>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 教育背景：学历、学校、专业 -->
        <el-row :gutter="10">
          <el-col :span="8">
            <el-form-item prop="education" label="最高学历">
              <el-select
                v-model="infoForm.education"
                default-first-option
                placeholder="请选择"
              >
                <el-option
                  v-for="item in educationList"
                  :key="item"
                  :label="item"
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="school" label="学校名称">
              <el-input v-model="infoForm.school" placeholder="学校名称" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="major" label="专业名称">
              <el-input v-model="infoForm.major" placeholder="专业名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 期望薪资 + 所在城市 -->
        <el-row :gutter="10">
          <el-col :span="16">
            <el-form-item label="期望薪资">
              <el-col :span="10">
                <el-input v-model="infoForm.salary_min" type="number">
                  <template #append>千元</template>
                </el-input>
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">~</span>
              </el-col>
              <el-col :span="11">
                <el-input v-model="infoForm.salary_max" type="number">
                  <template #append>千元</template>
                </el-input>
              </el-col>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="city" label="所在城市">
              <el-input v-model="infoForm.city" placeholder="城市名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 简历文件上传 -->
        <el-row>
          <el-form-item label="简历文件">
            <input
              ref="resumeInput"
              type="file"
              accept=".txt, .pdf, .doc, .docx"
              @change="handleResumeChange"
            />
          </el-form-item>
        </el-row>

        <!-- 提交按钮 -->
        <div class="register_btn">
          <el-button
            color="var(--theme-primary-color)"
            size="large"
            @click="submitInfoForm(ruleFormRef)"
          >
            提 交
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.register_container {
  min-height: calc(100vh - 170px - 60px - 40px);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.el-input {
  --el-input-focus-border-color: var(--theme-primary-color);
}
.register_main {
  width: 500px;
  margin: 0 auto;
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
  padding: 20px;
}

.register_btn {
  text-align: center;
}
.register_btn button {
  width: 100%;
  margin-bottom: 10px;
}
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
.info_main {
  width: 800px;
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
  margin: 0 auto;
  padding: 20px;
}
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.text-center {
  text-align: center;
}

.image {
  height: 100%;
  width: 100%;
}
.preview {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 160px;
  margin: 0 auto;
  width: 80%;
  background-image: url('../../assets/avatar-placeholder.jpeg');
  background-size: cover;
  background-position: center;
}

.preview img {
  height: 100%;
  width: 100%;
}
</style>