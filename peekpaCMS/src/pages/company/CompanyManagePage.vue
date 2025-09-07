<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage,type FormInstance,type InputInstance } from 'element-plus';
import { nextTick, onMounted, reactive, ref } from 'vue';
import { UNAUTH_401 } from '../../services/Axios';
import { timeStampFormat } from '../../utils/helper';
import type { CompanyListResponse } from '../../types/Company';
import {
  getAllCompanies,
  createCompany,
  searchCompany,
} from '../../services/company';

const LIMIT = 10;
let curOffset = 0;

const data = ref<CompanyListResponse>();
const curPage = ref<number>(1);
const total = ref<number>(0);
const showCreate = ref<boolean>(false);
const createFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const search = ref<string>('');

// 请求数据逻辑
const requestData = async (offset: number) => {
  loading.value = true;
  try {
    const response = await getAllCompanies(LIMIT, offset);
    if (response.status === 200) {
      data.value = response.data;
      total.value = response.data.count;
      curPage.value = curOffset / LIMIT + 1;
    }
    loading.value = false;
  } catch (error) {
    if ((error as Error).message !== UNAUTH_401) {
      ElMessage.error(`网络请求错误[${error}]`);
    }
    loading.value = false;
  }
};

// 搜索公司逻辑
const searchData = async (q: string, offset: number) => {
  loading.value = true;
  try {
    const response = await searchCompany(q, LIMIT, offset);
    if (response.status === 200) {
      data.value = response.data;
      total.value = response.data.count;
      curPage.value = curOffset / LIMIT + 1;
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
  await requestData(0);
});

// 页面跳转方法
const handlePageChange = async (value: number) => {
  curOffset = (value - 1) * LIMIT;
  await requestData(curOffset);
};

// 公司创建方法
// 公司创建方法
const handleCreate = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await createCompany(createForm);
        if (response.status === 201) {
          ElMessage.success('创建成功');
          formEl.resetFields();
          showCreate.value = false;
          await searchData(search.value, curOffset);
        } else {
          ElMessage.error(`创建失败[${response.status}]`);
        }
      } catch (error) {
        ElMessage.error(`创建失败[${(error as AxiosError).response?.status}]`);
      }
    } else {
      ElMessage.error('请仔细检查表单');
    }
  });
};
// 处理对话框焦点方法
const handleDialogOpen = () => {
  nextTick(() => {
    if (dialogInput.value) {
      dialogInput.value.focus();
    }
  });
};

// 搜索方法
const handleSearch = async () => {
  curOffset = 0;
  await searchData(search.value, curOffset);
};

// 清空搜索栏
const clearSearch = async () => {
  curOffset = 0;
  await requestData(curOffset);
};

// 格式化显示时间
const displayTime = (time: string) => {
  if (!time) return time;
  return timeStampFormat(time);
};

// 显示公司创建方法
const showCreateWindow = () => {
  showCreate.value = true;
};

interface CreateUserForm {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  company: string;
  website: string;
  name: string;
}

const createForm = reactive<CreateUserForm>({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  company: '',
  website: '',
  name: '',
});

const dialogInput = ref<InputInstance>();

// 处理对话框焦点方法

</script>
<template>
  <div class="container">
    <el-row class="search_main">
      <el-col :span="6">
        <el-button
          icon="CirclePlusFilled"
          type="primary"
          @click="showCreateWindow()"
          >创建新公司</el-button
        >
      </el-col>
      <el-col :span="6" :offset="12">
        <el-input
          v-model="search"
          prefix-icon="Search"
          placeholder="搜索"
          clearable
          @keyup.enter="handleSearch"
          @clear="clearSearch"
        />
      </el-col>
    </el-row>

    <el-table
      v-loading="loading"
      border
      header-cell-class-name="table-header"
      :data="data?.results"
    >
      <el-table-column label="公司名称">
        <template #default="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="公司网址" width="300">
        <template #default="scope">
          <el-link :href="scope.row.website" target="_blank">
            {{ scope.row.website }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column label="联系人姓名" width="100">
        <template #default="scope">
          <div v-if="scope.row.user">
            {{ scope.row.user.last_name ?? '' }}{{ scope.row.user.first_name ?? '' }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="联系人邮箱" width="200">
        <template #default="scope">
          <div v-if="scope.row.user">
            {{ scope.row.user.email }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="180">
        <template #default="scope">
          <div v-if="scope.row.user">
            {{ displayTime(scope.row.user.data_join ?? '') }}
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="pagination_main"
      background
      layout="prev, pager, next"
      :current-page="curPage"
      :total="total"
      :page-size="LIMIT"
      @current-change="handlePageChange"
    />

    <el-dialog
      v-model="showCreate"
      title="创建新用户"
      width="50%"
      @open="handleDialogOpen"
    >
      <el-form ref="createFormRef" :model="createForm" label-position="top">
        <el-form-item label="公司名称" prop="name">
          <el-input ref="dialogInput" v-model="createForm.name" />
        </el-form-item>
        <el-form-item label="公司网站" prop="website">
          <el-input v-model="createForm.website" />
        </el-form-item>
        <el-form-item label="姓" prop="last_name">
          <el-input v-model="createForm.last_name" />
        </el-form-item>
        <el-form-item label="名" prop="first_name">
          <el-input v-model="createForm.first_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="createForm.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="createForm.password" type="password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreate = false">取消</el-button>
          <el-button type="primary" @click="handleCreate(createFormRef)">
            提交
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.pagination_main {
  margin-top: 20px;
}

.search_main {
  margin-bottom: 20px;
}
</style>


