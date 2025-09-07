<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { onMounted, reactive, ref } from 'vue';
import { UNAUTH_401 } from '../../services/Axios';
import { getUserInfo, updateUserInfo } from '../../services/user';
import type{ UserSetting } from '../../types/User';
import useStore from '../../store/modules/User';

const userStore = useStore();

const previewInput = ref<HTMLInputElement | null>(null);
const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const isManager = ref<boolean>(false);

const form = reactive<UserSetting>({
  avatar: '',
  name: '',
  description: '',
  size: '',
  slogan: '',
  tags: [],
  website: '',
  password: '',
  user: {
    email: '',
    name: '',
    gender: 0,
  },
});

// 公司规模
const companySize = [
  '10人以下',
  '10~50人',
  '50~100人',
  '100~500人',
  '500~2000人',
  '2000~10000人',
  '10000人以上',
];

// 公司标签多选框列表内容
const companyLabelList = [
  '游戏',
  '社交平台',
  '区块链',
  '金融业',
  '影视',
  '电商平台',
  '短视频',
  '直播平台',
];

// 请求用户数据方法
const requestData = async () => {
  loading.value = true;
  try {
    const response = await getUserInfo();
    if (response.status === 200) {
      const protocol = import.meta.env.VITE_BASE_PROTOCOL; // 获取协议
      const host = import.meta.env.VITE_BASE_HOST; // 获取主机名和端口号
      const baseURL = `${protocol}://${host}`;
      form.avatar = `${baseURL}/${response.data.avatar}`;
      form.name = response.data.name;
      form.description = response.data.description;
      form.size = response.data.size;
      form.slogan = response.data.slogan;
      form.tags = response.data.tags
        ? (response.data.tags as string).split(',')
        : [];
      form.website = response.data.website;
      form.user = response.data.user;
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
  const user = userStore.getUser;
  if (user) {
    isManager.value = user.is_manager;
  }
});

// 用户信息修改逻辑
const handleSubmit = async () => {
  loading.value = true;
  try {
    const updateData = new FormData();
    if (form.password) {
        updateData.append('password', form.password);
    }
    if (isManager.value) {
      updateData.append('slogan', form.slogan);
      updateData.append('size', form.size);
      updateData.append('description', form.description);
      updateData.append('tags', (form.tags as string[]).join(','));
      if (form.avatar_file) {
        updateData.append('avatar_file', form.avatar_file);
      }
    }
    const response = await updateUserInfo(updateData);
    if (response.status === 200) {
      ElMessage.success('修改成功');
      // 重置表单
      ruleFormRef.value?.resetFields();
    } else {
      ElMessage.error(`修改失败[${response.status}]`);
    }
    loading.value = false;
  } catch (error) {
    ElMessage.error(`修改失败[${(error as AxiosError).message}]`);
    loading.value = false;
  }
};

// 选中上传图片文件
const previewImage = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length) {
    const file = target.files[0];
    form.avatar = URL.createObjectURL(file);
    form.avatar_file = file;
  }
};

// 触发 input 组件上传图片文件
const uploadPreview = () => {
  if (previewInput.value) {
    previewInput.value.click();
  }
};
</script>

<template>
  <div class="container">
    <el-form
      ref="ruleFormRef"
      v-loading="loading"
      class="form-box"
      :model="form"
      label-width="auto"
      label-position="top"
    >
      <el-row v-if="isManager" :gutter="40">
        <el-col :span="12">
          <el-form-item label="公司名称" prop="title">
            <el-input v-model="form.name" disabled></el-input>
          </el-form-item>
          <el-form-item label="公司口号" prop="title">
            <el-input v-model="form.slogan"></el-input>
          </el-form-item>

          <el-form-item label="公司网址" prop="title">
            <el-input v-model="form.website" disabled></el-input>
          </el-form-item>

          <el-row :gutter="20">
            <el-col :span="16">
              <el-form-item label="公司标签" prop="title">
                <el-select
                  v-model="form.tags"
                  multiple
                  :multiple-limit="3"
                  placeholder="请选择(多选，最多三个)"
                  style="width: 100%"
                >
                  <el-option
                    v-for="item in companyLabelList"
                    :key="item"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="公司规模" prop="title">
                <el-select v-model="form.size">
                  <el-option
                    v-for="item in companySize"
                    :key="item"
                    class=""
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="8">
          <el-form-item label="公司头像" prop="title">
            <input
              id="avater"
              ref="previewInput"
              name="avater"
              type="file"
              hidden
              accept=".png, .jpg, .jepg"
              @change="previewImage"
            />
            <div class="preview_container" @click="uploadPreview">
              <el-image class="preview" :src="form.avatar" fit="fill">
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
          </el-form-item></el-col
        >
      </el-row>

      <el-form-item v-if="isManager" label="公司简介" prop="title">
        <el-input
          v-model="form.description"
          :autosize="{ minRows: 4 }"
          type="textarea"
        ></el-input>
      </el-form-item>

      <el-form-item label="登录邮箱" prop="title">
        <el-input v-model="form.user.email" disabled></el-input>
      </el-form-item>

      <el-form-item label="姓名" prop="title">
        <el-input v-model="form.user.name" disabled></el-input>
      </el-form-item>

      <el-form-item label="新密码" prop="title">
        <el-input v-model="form.password" type="password"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<style scoped>
.preview_container {
  width: 200px;
}
.preview {
  height: 200px;
  width: 100%;
  background-size: cover;
}

.image-error {
  width: 100%;
  height: 100%;
  background-color: #dfdfdf;
  text-align: center;
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.preview img {
  height: 100%;
  width: 100%;
}
</style>