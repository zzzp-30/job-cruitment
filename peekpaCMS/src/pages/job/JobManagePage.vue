<script setup lang="ts">
import { AxiosError } from 'axios';
import {
  ElMessage,
  ElMessageBox,
} from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { UNAUTH_401 } from '../../services/Axios';
import { getAllJobs, updateJob, searchJob } from '../../services/job';
import { timeStampFormat } from '../../utils/helper';
import type { ResponseJobList, Job } from '../../types/Job';
import ROUTER_CONSTANTS from '../../route/constants';

// 全局路由
const router = useRouter();

const LIMIT = 10;
let curOffset = 0;

const STATUS_LIST_JOB = [
  {
    value: 0,
    label: '已发布',
  },
  {
    value: 1,
    label: '已下线',
  },
  {
    value: 2,
    label: '已结束',
  },
];

const data = ref<ResponseJobList>();
const curPage = ref<number>(1);
const total = ref<number>(0);
const showUpdate = ref<boolean>(false);
const loading = ref<boolean>(false);
const search = ref<string>('');

// 请求职位数据
const requestData = async (offset: number) => {
  loading.value = true;
  try {
    const response = await getAllJobs(LIMIT, offset);
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

// 搜索职位
const searchData = async (q: string, offset: number) => {
  loading.value = true;
  try {
    const response = await searchJob(q, LIMIT, offset);
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

const handlePageChange = async (value: number) => {
  curOffset = (value - 1) * LIMIT;
  await requestData(curOffset);
};

// 显示修改对话框
const showUpdateWindow = (index: number, item: Job) => {
  showUpdate.value = true;
  updateForm.index = index;
  updateForm.id = item.id;
  updateForm.title = item.title;
  updateForm.status = item.status;
  updateForm.city = item.city;
  updateForm.location = item.location;
  updateForm.salary_count = item.salary_count;
  updateForm.salary_min = item.salary_min;
  updateForm.salary_max = item.salary_max;
  updateForm.hire_number = item.hire_number;
  updateForm.pass_number = item.pass_number;
  updateForm.education = item.education;
  updateForm.experience = item.experience;
  updateForm.benefit = item.benefit;
  updateForm.description = item.description;
  updateForm.publish_time = item.publish_time;
  updateForm.resumes = item.resumes;
};
// 职位下线操作
const handleDelete = (index: number, item: Job) => {
  ElMessageBox.confirm(`确定要下线“${item.title}”么?`, '警告', {
    confirmButtonText: '下线',
    cancelButtonText: '取消',
    type: 'error',
  })
    .then(async () => {
      const response = await updateJob(item.id, {
        status: STATUS_LIST_JOB[2].value,
      });
      if (response.status === 200) {
        ElMessage.success('下线成功');
        if (data.value?.results) {
          data.value.results[index].status = STATUS_LIST_JOB[2].value;
        }
      } else {
        ElMessage.error(`下线失败[${response.status}]`);
      }
    })
    .catch((error: any) => {
      if (
        (error as AxiosError).name !== 'CanceledError' &&
        error !== 'cancel'
      ) {
        ElMessage.error('下线网络错误');
      }
    });
};

// 快速更改状态
const statusChange = async (status: number, id: string) => {
  try {
    const response = await updateJob(id, { status });
    if (response.status === 200) {
      ElMessage.success('更新成功');
    } else {
      ElMessage.error(`更新失败`);
    }
  } catch (error) {
    ElMessage.error('发生错误');
  }
};

// 禁止职位修改
const diableOperation = (item: Job) => {
  return item.status === 1 || item.status === 2;
};

// 显示职位招聘进度
const displayProgress = (item: Job) => {
  return `${item.pass_number}/${item.hire_number}`;
};

// 格式化时间
const formatTimestamp = (time: string) => {
  return timeStampFormat(time);
};

const handleDialogOpen = () => {
  
};

// 格式化薪水
const displaySalary = (item: Job) => {
  const max = Number((item.salary_max / 1000).toFixed(1));
  const min = Number((item.salary_min / 1000).toFixed(1));
  return max === min
    ? `${max}k/月 ${item.salary_count}薪`
    : `${min}k~${max}k/月 ${item.salary_count}薪`;
};

// 出发搜索请求
const handleSearch = async () => {
  curOffset = 0;
  await searchData(search.value, curOffset);
};

// 清空搜索
const clearSearch = async () => {
  curOffset = 0;
  await requestData(curOffset);
};
 
// 跳转到面试管理页面
const showInterviewManagePage = (id: string) => {
  router.push({
    name: ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE,
    query: {
      jobId: id,
    },
  });
};
interface UpdateJobForm extends Job {
  index: number;
}
import { reactive } from 'vue';

const updateForm = reactive<UpdateJobForm>({
  index: -1,
  id: '-1',
  title: '',
  status: -1,
  city: '',
  location: '',
  salary_min: -1,
  salary_max: -1,
  salary_count: -1,
  hire_number: -1,
  pass_number: -1,
  experience: '',
  benefit: '',
  education: '',
  description: '',
  publish_time: '',
  resumes: 0,
});

const experienceList = [
  '不需要经验',
  '经验0-2年',
  '经验2-5年',
  '经验5-10年',
  '经验10年以上',
];

const educationList = ['博士', '研究生', '大学', '高中', '初中', '初中以下'];

import type { FormInstance } from 'element-plus';

const updateFormRef = ref<FormInstance>();

// 职位修改功能
const handleUpdate = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const updateData: { [key: string]: string | number } = {};
        Object.entries(updateForm).forEach(([key, value]) => {
          if (typeof value === 'string' || typeof value === 'number') {
            updateData[key] = value;
          }
        });
        const response = await updateJob(updateForm.id, updateData);
        if (response.status === 200) {
          ElMessage.success('更新成功');
          showUpdate.value = false;
          const { index } = updateForm;
          if (data.value !== undefined) {
            // 更新列表数据  
            data.value.results[index] = response.data;
          }
          updateForm.index = -1;
          formEl.resetFields();
        } else {
          ElMessage.error(`更新失败[${response.status}]`);
        }
      } catch (error) {
        ElMessage.error(`更新失败`);
      }
    } else {
      ElMessage.error('请仔细检查表单');
    }
  });
};
</script>

<template>
  <div class="container">
    <!-- 搜索区域 -->
    <el-row class="search_main">
      <el-col :span="6" :offset="18">
        <el-input
          v-model="search"
          prefix-icon="eli-Search"
          placeholder="搜索"
          clearable
          @keyup.enter="handleSearch"
          @clear="clearSearch"
        />
      </el-col>
    </el-row>

    <!-- 数据表格 -->
    <el-table
      v-loading="loading"
      border
      header-cell-class-name="table-header"
      :data="data?.results"
    >
      <el-table-column prop="id" label="#" width="100" />

      <!-- 职位名称 -->
      <el-table-column prop="title" label="职位名称">
        <template #default="scope">
          <el-link type="primary">{{ scope.row.title }}</el-link>
        </template>
      </el-table-column>

      <!-- 薪资 -->
      <el-table-column label="薪资">
        <template #default="scope">
          {{ displaySalary(scope.row) }}
        </template>
      </el-table-column>

      <!-- 收到简历 -->
      <el-table-column label="收到简历" width="90">
        <template #default="scope">
          {{ scope.row.resumes }} 份
        </template>
      </el-table-column>

      <!-- 招聘进度 -->
      <el-table-column label="招聘进度" width="90">
        <template #default="scope">
          {{ displayProgress(scope.row) }}
        </template>
      </el-table-column>

      <!-- 状态 -->
      <el-table-column label="状态" width="100">
        <template #default="scope">
          <el-select
            v-model="scope.row.status"
            :disabled="diableOperation(scope.row)"
            size="small"
            @change="statusChange($event, scope.row.id)"
          >
            <el-option
              v-for="item in STATUS_LIST_JOB"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </template>
      </el-table-column>

      <!-- 创建日期 -->
      <el-table-column prop="publish_time" label="创建日期" width="170">
        <template #default="scope">
          {{ formatTimestamp(scope.row.publish_time) }}
        </template>
      </el-table-column>

      <!-- 操作 -->
      <el-table-column width="270">
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <div>操作</div>
          </div>
        </template>
        <template #default="scope">
          <el-button
            size="small"
            icon="eli-document"
            type="primary"
            plain
            :disabled="diableOperation(scope.row)"
            @click="showInterviewManagePage(scope.row.id)"
          >
            面试管理
          </el-button>
          <el-button
            size="small"
            icon="eli-setting"
            type="warning"
            plain
            :disabled="diableOperation(scope.row)"
            @click="showUpdateWindow(scope.$index, scope.row)"
          >
            修改
          </el-button>
          <el-button
            size="small"
            type="danger"
            icon="eli-delete"
            plain
            :disabled="diableOperation(scope.row)"
            @click="handleDelete(scope.$index, scope.row)"
          >
            下线
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      class="pagination_main"
      background
      layout="prev, pager, next"
      :current-page="curPage"
      :total="total"
      :page-size="LIMIT"
      @current-change="handlePageChange"
    />

    <!-- 修改弹窗 -->
    <el-dialog
      v-model="showUpdate"
      title="修改"
      width="50%"
      @open="handleDialogOpen"
    >
      <el-form ref="updateFormRef" :model="updateForm">
        <el-form-item label="职位名称">
          <el-input ref="dialogInput" v-model="updateForm.title" />
        </el-form-item>

        <el-form-item label="工作地点">
          <el-col :span="5">
            <el-input v-model="updateForm.city" placeholder="城市" />
          </el-col>
          <el-col :span="1" />
          <el-col :span="18">
            <el-input v-model="updateForm.location" placeholder="地址" />
          </el-col>
        </el-form-item>

        <el-form-item label="职位薪资">
          <el-col :span="6">
            <el-input v-model="updateForm.salary_min" type="number">
              <template #append>元</template>
            </el-input>
          </el-col>
          <el-col :span="1" class="text-center">
            <span class="text-gray-500">~</span>
          </el-col>
          <el-col :span="6">
            <el-input v-model="updateForm.salary_max" type="number">
              <template #append>元</template>
            </el-input>
          </el-col>
          <el-col :span="2" class="text-right">
            <span>一年</span>
          </el-col>
          <el-col :span="5">
            <el-input v-model="updateForm.salary_count" type="number" :min="12" :max="50">
              <template #append>薪</template>
            </el-input>
          </el-col>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="经验要求" prop="experience">
              <el-select v-model="updateForm.experience">
                <el-option
                  v-for="item in experienceList"
                  :key="item"
                  :label="item"
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="学历要求" prop="education">
              <el-select v-model="updateForm.education">
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
            <el-form-item label="招聘人数" prop="hire">
              <el-input-number
                v-model="updateForm.hire_number"
                :min="1"
                :max="100"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="职位福利" prop="benefit">
          <el-input
            v-model="updateForm.benefit"
            type="textarea"
            :autosize="{ minRows: 2 }"
          />
        </el-form-item>

        <el-form-item label="具体要求" prop="description">
          <el-input
            v-model="updateForm.description"
            type="textarea"
            :autosize="{ minRows: 4 }"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showUpdate = false">取消</el-button>
          <el-button type="primary" @click="handleUpdate(updateFormRef)">
            更新
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