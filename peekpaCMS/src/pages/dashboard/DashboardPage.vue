<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';
import ClockComponent from '../../components/ClockComponent.vue';
import DashboardCardComponent from '../../components/DashboardCardComponent.vue';
import { type DashboardResponse } from '../../types/Dashboard';
import { UNAUTH_401 } from '../../services/Axios';
import getDashboard from '../../services/dashboard';
import { timeStampFormat } from '../../utils/helper';

// 数据响应式
const data = ref<DashboardResponse | null>(null); // 初始为 null 更清晰
const loading = ref<boolean>(false);

// 请求首页数据
const requestData = async () => {
  loading.value = true;
  try {
    const response = await getDashboard();
    if (response.status === 200) {
      data.value = response.data; // 假设 response 是 axios 响应
    } else {
      ElMessage.warning('数据加载失败，请稍后重试');
    }
  } catch (error) {
    if ((error as Error).message !== UNAUTH_401) {
      ElMessage.error(`网络请求错误：${error}`);
    }
  } finally {
    loading.value = false; // 统一在 finally 中关闭 loading
  }
};

// 构建职位链接
const getUrl = (id: string) => {
  return `http://localhost:8001/$/job/${id}/`;
};

// 格式化时间显示
const displayTime = (time: string) => {
  return timeStampFormat(time);
};

// 页面挂载后请求数据
onMounted(async () => {
  await requestData();
});
</script>

<template>
  <div class="container">
    <!-- 第一行：关键指标 -->
    <el-row :gutter="20" class="dashboar_row">
      <el-col :span="6">
        <ClockComponent />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="今日新增简历"
          :count="data?.resumes_new ?? 0"
          icon="eli-Box"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="已经招聘人数"
          :count="data?.pass_number ?? 0"
          icon="eli-GoldMedal"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="预计招聘人数"
          :count="data?.hired_number ?? 0"
          icon="eli-Medal"
        />
      </el-col>
    </el-row>

    <!-- 第二行：职位状态 -->
    <el-row :gutter="20" class="dashboar_row">
      <el-col :span="6">
        <DashboardCardComponent
          title="职位总数"
          :count="data?.jobs_total ?? 0"
          icon="eli-Folder"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="开放职位"
          :count="data?.jobs_open ?? 0"
          icon="eli-FolderOpened"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="已招满职位"
          :count="data?.jobs_finish ?? 0"
          icon="eli-FolderChecked"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="已下线职位"
          :count="data?.jobs_close ?? 0"
          icon="eli-FolderDelete"
        />
      </el-col>
    </el-row>

    <!-- 第三行：招聘流程 -->
    <el-row :gutter="20" class="dashboar_row">
      <el-col :span="6">
        <DashboardCardComponent
          title="共收到简历"
          :count="data?.resumes ?? 0"
          icon="eli-Notebook"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="面试数"
          :count="data?.interviewing ?? 0"
          icon="eli-DataLine"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="发出邀请数"
          :count="data?.invitation_number ?? 0"
          icon="eli-Stopwatch"
        />
      </el-col>
      <el-col :span="6">
        <DashboardCardComponent
          title="公司总人数"
          :count="data?.users_number ?? 0"
          icon="eli-User"
        />
      </el-col>
    </el-row>

    <!-- 第四行：表格 -->
    <el-row :gutter="20" class="dashboar_row">
      <!-- 最新职位 -->
      <el-col :span="12">
        <div class="table_title">最新职位信息</div>
        <el-table
          border
          header-cell-class-name="table-header"
          :data="data?.new_jobs || []"
        >
          <el-table-column label="职位名称">
            <template #default="scope">
              <el-link
                type="primary"
                target="_blank"
                :href="getUrl(scope.row.id)"
              >
                {{ scope.row.title }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column label="发布日期" width="200">
            <template #default="scope">
              {{ displayTime(scope.row.publish_time) }}
            </template>
          </el-table-column>
        </el-table>
      </el-col>

      <!-- 最新简历岗位 -->
      <el-col :span="12">
        <div class="table_title">最新简历岗位</div>
        <el-table
          border
          header-cell-class-name="table-header"
          :data="data?.new_interviews || []"
        >
          <el-table-column label="职位名称">
            <template #default="scope">
              <el-link
                type="primary"
                target="_blank"
                :href="getUrl(scope.row.id)"
              >
                {{ scope.row.title }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column label="发布日期" width="200">
            <template #default="scope">
              {{ displayTime(scope.row.publish_time) }}
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dashboar_row {
  margin-bottom: 20px;
}

.table_title {
  margin-bottom: 15px;
  font-weight: 500;
  font-size: 1.3rem;
}
</style>