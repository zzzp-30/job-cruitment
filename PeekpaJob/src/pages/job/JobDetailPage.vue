<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { ElMessage } from 'element-plus';
import type { JobDetailResponse } from '../../types/Job';
import { getJobDetail, applyJob } from '../../services/job';
import useStore from '../../store/modules/User';
import ROUTER_CONSTANTS from '../../route/constants';

const route = useRoute();
const router = useRouter();
const userStore = useStore();
const data = ref<JobDetailResponse>();
const loading = ref<boolean>(true);

// 请求数据
const requestData = async (jobId: string) => {
  try {
    loading.value = true;
    const response = await getJobDetail(jobId);
    if (response.status === 200) {
      data.value = response.data;
    }

    loading.value = false;
    window.scrollTo(0, 0);
  } catch (error) {
    loading.value = false;
    // 这里可以自定义网络请求错误处理
    console.error(error);
  }
};

onMounted(() => {
  requestData(route.params.jobId as string);
});

// 格式化显示职位薪水
const displaySalary = (item: JobDetailResponse) => {
  const max = Number((item.salary_max / 1000).toFixed(1));
  const min = Number((item.salary_min / 1000).toFixed(1));
  if (max === min) {
    return `${max}K / ${item.salary_count}薪`;
  }
  return `${min}K~${max}K / ${item.salary_count}薪`;
};

// 格式化系那是发布时间
const displayTime = (item: JobDetailResponse) => {
  const dateTime = new Date(item.publish_time);
  const YY = String(dateTime.getFullYear()).padStart(4, '0');
  const MM = String(dateTime.getMonth() + 1).padStart(2, '0');
  const DD = String(dateTime.getDate()).padStart(2, '0');
  const hh = String(dateTime.getHours()).padStart(2, '0');
  const mm = String(dateTime.getMinutes()).padStart(2, '0');
  const ss = String(dateTime.getSeconds()).padStart(2, '0');
  return `${YY}/${MM}/${DD} ${hh}:${mm}:${ss}`;
};

// 格式化显示公司标签
const displayCompanyTags = (item: JobDetailResponse) => {
  return item.company_tags.replace(new RegExp(',', 'g'), ' | ');
};

// 公司详情页地址
const getCompanyURL = (item: JobDetailResponse) => {
  const baseUrl = import.meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/#/company/${item.company_id}`;
};
// 跳转至登录页
const goToLogin = () => {
  router.push({
    name: ROUTER_CONSTANTS.SIGN_IN,
    query: {
      next: route.fullPath,
    },
  });
};

// 跳转至个人信息页面
const goToProfile = () => {
  router.push({
    name: ROUTER_CONSTANTS.PROFILE,
  });
};

// 职位申请
const handleApply = async () => {
  try {
    // 请求数据
    if (data.value) {
      const response = await applyJob(data.value.id);
      if (response.status === 200) {
        ElMessage.success('申请成功');
        data.value.applied = true;
      } else {
        ElMessage.error(`投简失败[${response.status}]`);
      }
    }
  } catch (error) {
    ElMessage.error('发生错误');
  }
};
</script>

<template>
  <div class="index_container">
    <div v-if="data">
      <div class="info_block">
        <div class="title_line">
          {{ data.title }} <span class="salary">{{ displaySalary(data) }}</span>
        </div>
        <div class="location_line">
          <div>
            {{ data.city }} / {{ data.experience }} / {{ data.education }}
          </div>
          <div v-if="userStore.isLogin() == false" class="button">
            <el-button type="primary" size="large" @click="goToLogin"
              >请登录之后再投简历</el-button
            >
          </div>
          <div v-else-if="data.applied" class="button">
            <el-button type="primary" size="large" disabled>已申请</el-button>
          </div>
          <div v-else-if="data.has_resume" class="button">
            <el-button type="primary" size="large" @click="handleApply"
              >投简历</el-button
            >
          </div>
          <div v-else class="button">
            <el-button type="primary" size="large" @click="goToProfile"
              >投简历需要首先上传简历</el-button
            >
          </div>
        </div>
        <div class="company_line">
          <el-link :href="getCompanyURL(data)" target="_blank" class="link">{{
            data.company_name
          }}</el-link>
          <span class="time">发布于：{{ displayTime(data) }}</span>
        </div>
      </div>
      <el-row :gutter="20">
        <el-col :span="17">
          <el-row class="content_block">
            <el-col :span="24" class="block_title">职位诱惑</el-col>
            <el-col :span="24" class="description">
              <pre>{{ data.benefit }}</pre>
            </el-col>
            <el-col :span="24" class="block_title">职位描述</el-col>
            <el-col :span="24" class="description">
              <pre>{{ data.description }}</pre>
            </el-col>
            <el-col :span="24" class="block_title">工作地点</el-col>
            <el-col :span="24" class="description">
              <pre>{{ data.city }} - {{ data.location }}</pre>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="7">
          <el-row class="content_block">
            <el-col :span="24" class="block_title"
              >{{ data.company_name }}基本情况</el-col
            >
            <el-col :span="24" class="company_info"
              ><el-icon class="icon"><eli-PriceTag /></el-icon
              >{{ displayCompanyTags(data) }}</el-col
            >
            <el-col :span="24" class="company_info"
              ><el-icon class="icon"><eli-Position /></el-icon
              >{{ data.city }}</el-col
            >
            <el-col :span="24" class="company_info"
              ><el-icon class="icon"><eli-User /></el-icon
              >{{ data.company_size }}</el-col
            >
            <el-col :span="24" class="company_info"
              ><el-icon class="icon"><eli-Monitor /></el-icon
              ><el-link :href="data.company_website" target="_blank">{{
                data.company_website
              }}</el-link></el-col
            >
          </el-row></el-col
        >
      </el-row>
    </div>
    <div v-else-if="!loading && !data" class="failure">
      没有数据，请稍后再试
    </div>
  </div>
</template>

<style scoped>
.index_container {
  min-height: calc(100vh - 170px - 60px - 40px);
}

.info_block {
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.title_line {
  color: var(--theme-primary-color);
  font-size: 1.5rem;
  font-weight: bold;
}

.salary {
  font-size: 1.3rem;
  color: #e31117;
  font-weight: 700;
}

.time {
  margin-left: 20px;
  font-size: 0.9rem;
  color: #929292;
}

.location_line {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.content_block {
  margin-top: 20px;
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
  padding: 20px;
}

.description {
  margin-top: 20px;
  margin-bottom: 20px;
  font-size: 1rem;
}

.block_title {
  font-size: 1.3rem;
  font-weight: bold;
  color: var(--theme-primary-color);
}

.company_info {
  margin-top: 20px;
}

.icon {
  margin-right: 10px;
}

.link {
  font-size: 1rem;
}
.failure {
  text-align: center;
  margin-top: 250px;
  color: var(--theme-primary-color);
  font-weight: bolder;
}

pre {
  white-space: pre-line;
}
</style>