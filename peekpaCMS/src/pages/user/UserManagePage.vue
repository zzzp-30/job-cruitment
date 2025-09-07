<script setup lang="ts">
import { AxiosError } from 'axios';
import {
  ElMessage,
  ElMessageBox,
  type FormInstance,
  type InputInstance,
} from 'element-plus';
import { nextTick, onMounted, reactive, ref } from 'vue';
import { UNAUTH_401 } from '../../services/Axios';
import {
  getAllUsers,
  searchUser,
  updateUser,
  createUser,
} from '../../services/user';
import { timeStampFormat } from '../../utils/helper';
import type { UserListResponse, User } from '../../types/User';

const LIMIT = 10;
let curOffset = 0;

const data = ref<UserListResponse>();
const curPage = ref<number>(1);
const total = ref<number>(0);
const showCreate = ref<boolean>(false);
const dialogInput = ref<InputInstance>();
const loading = ref<boolean>(false);
const search = ref<string>('');

// 请求用户列表
const requestData = async (offset: number) => {
  loading.value = true;
  try {
    const response = await getAllUsers(LIMIT, offset);
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

// 搜索用户
const searchData = async (q: string, offset: number) => {
  loading.value = true;
  try {
    const response = await searchUser(q, LIMIT, offset);
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

const isDisable = (item: User) => {
  return !item.is_active;
};

onMounted(async () => {
  await requestData(0);
});

const handlePageChange = async (value: number) => {
  curOffset = (value - 1) * LIMIT;
  await requestData(curOffset);
};

// 禁止用户
const handleDelete = (index: number, item: User) => {
  ElMessageBox.confirm(
    `确定要禁止 ${item.last_name}${item.first_name} 登录系统?`,
    '警告',
    {
      confirmButtonText: '禁止',
      cancelButtonText: '取消',
      type: 'error',
    }
  )
    .then(async () => {
      const response = await updateUser(item.uid, {
        is_active: false,
      });
      if (response.status === 200) {
        ElMessage.success('操作成功');
        if (data.value?.results) {
          data.value.results[index].is_active = false;
        }
      } else {
        ElMessage.error(`操作失败[${response.status}]`);
      }
    })
    .catch((error) => {
      if (
        (error as AxiosError).name !== 'CanceledError' &&
        error !== 'cancel'
      ) {
        ElMessage.error('发生网络错误');
      }
    });
};

// 显示用户创建窗口
const handleDialogOpen = () => {
  nextTick(() => {
    if (dialogInput.value) {
      dialogInput.value.focus();
    }
  });
};

// 搜索用户
const handleSearch = async () => {
  curOffset = 0;
  await searchData(search.value, curOffset);
};

// 清空搜索框
const clearSearch = async () => {
  curOffset = 0;
  await requestData(curOffset);
};

// 显示性别
const displayGender = (gender: number) => {
  if (gender === 1) {
    return '男';
  }
  if (gender === 2) {
    return '女';
  }
  return '未设定';
};

// 格式化实现
const displayTime = (time: string) => {
  return timeStampFormat(time);
};

// 显示状态
const displayActive = (active: boolean) => {
  return active ? '允许' : '不允许';
};

const showCreateWindow = () => {
  showCreate.value = true;
};
const createFormRef = ref<FormInstance>();

const genderList = [
  {
    name: '未设置',
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
interface CreateUserForm {
  first_name: string;
  last_name: string;
  email: string;
  gender: number;
  password: string;
}

const createForm = reactive<CreateUserForm>({
  first_name: '',
  last_name: '',
  email: '',
  gender: 0,
  password: '',
});

// 新建用户
const handleCreate = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await createUser(createForm);
        if (response.status === 201) {
          ElMessage.success('创建成功');
          showCreate.value = false;
          await searchData(search.value, curOffset);
          formEl.resetFields();
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
</script>
<template>
  <div class="container">
    <el-row class="search_main">
      <el-col :span="6">
        <el-button
          icon="eli-CirclePlusFilled"
          type="primary"
          @click="showCreateWindow()"
          >创建用户</el-button
        >
      </el-col>
      <el-col :span="6" :offset="12">
        <el-input
          v-model="search"
          prefix-icon="eli-Search"
          placeholder="搜索"
          clearable
          @keyup.enter="handleSearch"
          @clear="clearSearch"
      /></el-col>
    </el-row>

    <el-table
      v-loading="loading"
      border
      header-cell-class-name="table-header"
      :data="data?.results"
    >
      <el-table-column label="姓名">
        <template #default="scope"
          >{{ scope.row.last_name }}{{ scope.row.first_name }}</template
        >
      </el-table-column>

      <el-table-column label="性别" width="80">
        <template #default="scope">
          {{ displayGender(scope.row.gender) }}
        </template>
      </el-table-column>
      <el-table-column label="邮箱" prop="email" width="200"> </el-table-column>

      <el-table-column label="注册时间" width="170">
        <template #default="scope">
          {{ displayTime(scope.row.data_join) }}
        </template>
      </el-table-column>

      <el-table-column label="最后登录" width="170">
        <template #default="scope">
          {{ displayTime(scope.row.last_login) }}
        </template>
      </el-table-column>

      <el-table-column label="允许登录" width="170">
        <template #default="scope">
          {{ displayActive(scope.row.is_active) }}
        </template>
      </el-table-column>

      <el-table-column>
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <div>操作</div>
          </div>
        </template>
        <template #default="scope">
          <el-button
            size="small"
            type="danger"
            icon="eli-close"
            plain
            :disabled="isDisable(scope.row)"
            @click="handleDelete(scope.$index, scope.row)"
            >禁止登录</el-button
          >
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
    ></el-pagination>
    <el-dialog
      v-model="showCreate"
      title="创建新用户"
      width="50%"
      @open="handleDialogOpen"
    >
    <el-form ref="createFormRef" :model="createForm" label-position="top">
    <el-form-item label="姓" prop="last_name">
        <el-input ref="dialogInput" v-model="createForm.last_name"></el-input>
    </el-form-item>
    <el-form-item label="名" prop="first_name">
        <el-input
        ref="dialogInput"
        v-model="createForm.first_name"
        ></el-input>
    </el-form-item>
    <el-form-item label="性别" prop="gender">
        <el-select
        v-model="createForm.gender"
        default-first-option
        placeholder="请选择"
        >
        <el-option
            v-for="item in genderList"
            :key="item.value"
            class=""
            :label="item.name"
            :value="item.value"
        ></el-option
        ></el-select>
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
        <el-input v-model="createForm.email"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
        <el-input v-model="createForm.password" type="password"></el-input>
    </el-form-item>
    </el-form>
    <template #footer>
    <span class="dialog-footer">
        <el-button @click="showCreate = false">取消</el-button>
        <el-button type="primary" @click="handleCreate(createFormRef)"
        >提交</el-button
        >
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