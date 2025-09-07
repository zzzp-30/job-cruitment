<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { UNAUTH_401 } from '../../services/Axios';
import { getUserInfo, updateUserInfo, uploadAvatar } from '../../services/user';
import { replyInvitation, uploadResume } from '../../services/job';
import { type UserApplication, type UserSetting } from '../../types/User';
import useStore from '../../store/modules/User';
import { type UpdateForm } from '../../types/base';
import ApplicationCard from '../../components/ApplicationCard.vue';
import avatarPlaceholder from '../../assets/avatar-placeholder.jpeg';
import router from '../../route';
import ROUTER_CONSTANTS from '../../route/constants';

// 用户管理
const userStore = useStore();

const previewResumeInput = ref<HTMLInputElement | null>(null);
const previewImageInput = ref<HTMLInputElement | null>(null);
const data = ref<UserSetting>();
const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const showUpdateWindow = ref<boolean>(false);

// 简历下载 URl
const resumeURL = computed(() => {
  const baseURL = import.meta.env.VITE_COMPANY_SITE_URL
  return `${baseURL}/${data.value?.resume.url}`;
});

// 请求个人数据
const requestData = async () => {
  loading.value = true;
  try {
    const response = await getUserInfo();
    if (response.status === 200) {
      data.value = response.data;
      updateForm.position = response.data.details.position;
      updateForm.education = response.data.details.education;
      updateForm.education = response.data.details.education;
      updateForm.school = response.data.details.school;
      updateForm.major = response.data.details.major;
      updateForm.experience_year = response.data.details.experience_year;
      updateForm.status = response.data.details.status;
      updateForm.city = response.data.details.city;
      updateForm.company_name = response.data.details.company_name;
      updateForm.company_name = response.data.details.company_name;
      updateForm.salary_min = response.data.details.salary_min;
      updateForm.salary_max = response.data.details.salary_max;
      updateForm.avatar = response.data.details.avatar;
      updateForm.phone = response.data.details.phone;
      updateForm.gender = response.data.gender;
      updateForm.name = `${response.data.last_name} ${response.data.first_name}`;
    }
    loading.value = false;
  } catch (error) {
    if ((error as Error).message !== UNAUTH_401) {
      ElMessage.error(`网络请求错误[${error}]`);
    }
    loading.value = false;
  }
};

onMounted(async () => {
  await requestData();
});

// 显示修改个人信息表单界面
const diaplayUpdateWindow = () => {
  showUpdateWindow.value = true;
};

// 触发简历上传
const uploadResumeClick = () => {
  if (previewResumeInput.value) {
    previewResumeInput.value.click();
  }
};

// 上传简历
const handleResumeFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length) {
    const file = target.files[0];
    try {
      const response = await uploadResume(file);
      if (response.status === 201) {
        ElMessage.success('简历上传成功');
        if (data.value) {
          data.value.resume.name = response.data.name;
          data.value.resume.url = response.data.url;
        }
      } else {
        ElMessage.error(`上传失败[${response.status}]`);
      }
    } catch (error) {
      ElMessage.error(`上传失败[${(error as AxiosError).message}]`);
    }
  }
};

// 提交面试邀请消息更新内容
const handleResponse = async (iid: string, value: number) => {
  if (data.value) {
    const index = data.value.applications.findIndex((app: UserApplication) => {
      if (app.invitation) {
        return app.invitation.id === iid;
      }
      return false;
    });
    if (index !== -1) {
      data.value.applications[index].invitation.response = value;
      try {
        // 请求数据
        if (data.value) {
          const response = await replyInvitation(iid, value);
          if (response.status !== 200) {
            ElMessage.error(`投简失败[${response.status}]`);
          }
        }
      } catch (error) {
        ElMessage.error('发生错误');
      }
    }
  }
};

// 监听当前是否有用户已经登录，如果没有登录，则跳转到登录页面
watch(
  () => userStore.isLogin(),
  async (newValue) => {
    if (!newValue) {
      await router.push({
        name: ROUTER_CONSTANTS.SIGN_IN,
      });
    }
  },
  { deep: true }
);

// 获取用户头像 URL
const getUserAvatar = (url: string) => {
  const baseUrl = import.meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/${url}`;
};
const experienceList = ['无经验', '2年以内', '2~5年', '5~10年', '10年以上'];

const statusList = ['目前状态', '在职', '已离职', '无业'];

const educationList = ['博士', '研究生', '大学', '高中', '初中', '初中以下'];

const updateForm = reactive<UpdateForm>({
  position: '',
  education: '',
  school: '',
  major: '',
  experience_year: '',
  status: '',
  city: '',
  company_name: '',
  salary_min: 0,
  salary_max: 0,
});


// 触发选择头像上传
const uploadPreview = () => {
  if (previewImageInput.value) {
    previewImageInput.value.click();
  }
};

// 头像上传
const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length) {
    const file = target.files[0];
    try {
      const response = await uploadAvatar(file);
      if (response.status === 201) {
        if (data.value) {
          updateForm.avatar = response.data.url;
        }
      } else {
        ElMessage.error(`头像上传失败[${response.status}]`);
      }
    } catch (error) {
      ElMessage.error(`头像上传失败[${(error as AxiosError).message}]`);
    }
  }
};

// 更新个人信息
const handleSubmit = async () => {
  loading.value = true;
  try {
    const response = await updateUserInfo(updateForm);
    if (response.status === 200) {
      ElMessage.success('修改成功');
      data.value = response.data;
      // 重置表单
      ruleFormRef.value?.resetFields();
      showUpdateWindow.value = false;
    } else {
      ElMessage.error(`修改失败[${response.status}]`);
    }
    loading.value = false;
  } catch (error) {
    ElMessage.error(`修改失败[${(error as AxiosError).message}]`);
    loading.value = false;
  }
};

// 关闭修改表单界面
const handleClose = () => {
  showUpdateWindow.value = false;
};
</script>
<template>
  <div class="index_container">
    <div v-if="data">
      <el-row class="line">
        <el-col :span="4">
          <el-image
            class="image"
            :src="data.details.avatar"
            fit="fill"
            :error="avatarPlaceholder"
            ><template #placeholder>
              <div class="image-slot">Loading<span class="dot">...</span></div>
            </template>
            <template #error>
              <div class="image-error">
                <el-icon><eli-Picture /></el-icon>
              </div> </template></el-image
        ></el-col>
        <el-col :span="20">
          <el-row class="title_line">
            <el-col :span="10" class="name"
              >{{ data.last_name }} {{ data.first_name }}</el-col
            >
            <el-col :span="4" :offset="10" class="text_right">
              <div v-if="data.details.city">
                <el-icon><eli-Location /></el-icon>{{ data.details.city }}
              </div></el-col
            >
          </el-row>
          <el-row>
            <el-col :span="2" class="item_title">联系邮箱:</el-col>
            <el-col :span="10">{{ data.email }}</el-col>
          </el-row>
          <el-row>
            <el-col :span="2" class="item_title">联系电话:</el-col>
            <el-col :span="10">{{ data.details.phone }}</el-col>
          </el-row>
          <el-row>
            <el-col :span="2" class="item_title">最高学历:</el-col>
            <el-col :span="10">{{ data.details.education }}</el-col>
          </el-row>
          <el-row>
            <el-col :span="2" class="item_title">目标职位:</el-col>
            <el-col :span="10">{{ data.details.position }}</el-col>
          </el-row>
          <el-row>
            <el-col :span="2" class="item_title">期望薪资:</el-col>
            <el-col :span="10"
              ><div v-if="data.details.salary_min">
                {{ data.details.salary_min }}k~{{ data.details.salary_max }}k
              </div></el-col
            >
            <el-col :span="2" :offset="10">
              <el-button type="info" plain @click="diaplayUpdateWindow"
                >修改信息</el-button
              >
            </el-col>
          </el-row>
        </el-col>
      </el-row>
      <el-row class="line">
        <el-col :span="2" :offset="1" class="resume_title">简历</el-col>
        <el-col v-if="data.resume" :span="10" class="resume"
          ><el-link type="info" target="_blank" :href="resumeURL">
            <el-icon><eli-Download /></el-icon> {{ data.resume.name }}</el-link
          ></el-col
        >
        <el-col v-else :span="10" class="no_resume">请先上传一份简历</el-col>
        <el-col :span="2" :offset="9" class="text-right"
          ><input
            ref="previewResumeInput"
            type="file"
            hidden
            accept=".txt, .pdf, .doc, .docx"
            @change="handleResumeFileChange"
          /><el-button type="info" plain @click="uploadResumeClick"
            >更新简历</el-button
          ></el-col
        >
      </el-row>
      <el-row class="line">
        <el-col :span="23" :offset="1" class="resume_title"
          >投递历史记录</el-col
        >
        <el-col
          v-for="item in data.applications"
          :key="item.id"
          :span="23"
          :offset="1"
        >
          <ApplicationCard
            :item="item"
            @update-response="handleResponse"
          ></ApplicationCard>
        </el-col>
      </el-row>
    </div>
  </div>

  <el-dialog
    v-model="showUpdateWindow"
    title="信息修改"
    width="50%"
  >
    <el-form
      ref="ruleFormRef"
      v-loading="loading"
      class="form-box"
      :model="updateForm"
      label-width="auto"
      label-position="top"
    >
      <el-row>
        <el-col :span="16">
          <el-row :gutter="10">
            <el-col :span="12"
              ><el-form-item prop="position" label="联系方式">
                <el-input v-model="updateForm.phone" placeholder="手机号">
                </el-input></el-form-item
            ></el-col>
            <el-col :span="10">
              <el-form-item prop="city" label="所在城市">
                <el-input v-model="updateForm.city" placeholder="城市名称">
                </el-input> </el-form-item
            ></el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="12"
              ><el-form-item prop="position" label="应聘职位">
                <el-input
                  v-model="updateForm.position"
                  placeholder="想要应聘的职位"
                >
                </el-input> </el-form-item
            ></el-col>
            <el-col :span="12">
              <el-form-item prop="status" label="目前状态">
                <el-select
                  v-model="updateForm.status"
                  default-first-option
                  placeholder="请选择"
                >
                  <el-option
                    v-for="item in statusList"
                    :key="item"
                    class=""
                    :label="item"
                    :value="item"
                  ></el-option
                ></el-select> </el-form-item
            ></el-col>
          </el-row>

          <el-row :gutter="10">
            <el-col :span="12">
              <el-form-item label="公司名称">
                <el-input
                  v-model="updateForm.company_name"
                  placeholder="现公司名称"
                >
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="experience_year" label="工作经验">
                <el-select
                  v-model="updateForm.experience_year"
                  default-first-option
                  placeholder="请选择"
                >
                  <el-option
                    v-for="item in experienceList"
                    :key="item"
                    class=""
                    :label="item"
                    :value="item"
                  ></el-option
                ></el-select>
              </el-form-item>
            </el-col> </el-row
        ></el-col>
        <el-col :span="8"
          ><el-form-item label="头像">
            <input
              ref="previewImageInput"
              type="file"
              hidden
              accept=".png, .jpg, .jepg"
              @change="handleFileChange"
            />
            <div class="image_wrapper" @click="uploadPreview">
              <el-image
                class="preview"
                :src="getUserAvatar(updateForm.avatar as string)"
                fit="fill"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><eli-Picture /></el-icon>
                  </div>
                </template>
                <template #placeholder>
                  <div class="image-slot">
                    Loading<span class="dot">...</span>
                  </div>
                </template></el-image
              >
            </div>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="8">
          <el-form-item prop="education" label="最高学历">
            <el-select
              v-model="updateForm.education"
              default-first-option
              placeholder="请选择"
            >
              <el-option
                v-for="item in educationList"
                :key="item"
                class=""
                :label="item"
                :value="item"
              ></el-option
            ></el-select> </el-form-item
        ></el-col>
        <el-col :span="8"
          ><el-form-item prop="school" label="学校名称">
            <el-input v-model="updateForm.school" placeholder="学校名称">
            </el-input> </el-form-item
        ></el-col>
        <el-col :span="8"
          ><el-form-item prop="major" label="专业名称">
            <el-input v-model="updateForm.major" placeholder="专业名称">
            </el-input> </el-form-item
        ></el-col>
      </el-row>

      <el-form-item label="期望薪资">
        <el-col :span="10">
          <el-input v-model="updateForm.salary_min" type="number"
            ><template #append>千元</template></el-input
          >
        </el-col>
        <el-col :span="2" class="text-center">
          <span class="text-gray-500">~</span>
        </el-col>
        <el-col :span="11">
          <el-input v-model="updateForm.salary_max" type="number">
            <template #append>千元</template></el-input
          >
        </el-col>
      </el-form-item>

      <el-form-item label="新密码" prop="title">
        <el-input v-model="updateForm.password" type="password"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">修改</el-button>
        <el-button type="danger" @click="handleClose">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<style scoped>
.preview {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 190px;
  width: 140px;
  margin: 0 auto;
  background-size: cover;
  background-position: center;
}

.text-center {
  text-align: center;
}
</style>