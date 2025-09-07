<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { getCompanyDetail } from '../../services/company';
import { type Job } from '../../types/Job';
import { type CompanyDetailResponse } from '../../types/Company';

// 页面数据
const data = ref<CompanyDetailResponse>();
const loading = ref<boolean>(true);

// 请求数据
const requestData = async (companyId: string) => {
  try {
    loading.value = true;
    const response = await getCompanyDetail(companyId);
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
  requestData(route.params.companyId as string);
});
// 路由对象
const route = useRoute();

// 格式化显示页面标签
const companyTags = computed(() => {
  return data.value ? data.value?.tags.split(',') : [];
});

// 格式化显示薪水
const displaySalary = (item: Job) => {
  const max = Number((item.salary_max / 1000).toFixed(1));
  const min = Number((item.salary_min / 1000).toFixed(1));
  if (max === min) {
    return `${max}K`;
  }
  return `${min}K~${max}K`;
};

// 格式化显示时间
const displayTime = (item: Job) => {
  const date: Date = new Date(item.publish_time);
  // 获取年、月、日、小时和分钟
  const year: number = date.getFullYear();
  const month: string = String(date.getMonth() + 1).padStart(2, '0');
  const day: string = String(date.getDate()).padStart(2, '0');
  const hours: string = String(date.getHours()).padStart(2, '0');
  const minutes: string = String(date.getMinutes()).padStart(2, '0');
  return `${year}年${month}月${day}日 ${hours}点${minutes}分`;
};


const getJobURL = (item: Job) => {
  const baseUrl = import.meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/#/job/${item.id}`;
};

const getCompanyAvatarURL = (url: string) => {
  const baseUrl = import.meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/${url}`;
}
</script>


<template>
  <div class="index_container">
    <div v-if="data">
      <el-row class="info_block">
        <el-col :span="4">
          <el-image
            class="image"
            :src="getCompanyAvatarURL(data.avatar)"
            fit="fill"
            ><template #placeholder>
              <div class="image-slot">Loading<span class="dot">...</span></div>
            </template></el-image
          >
        </el-col>
        <el-col :span="20" class="info_line">
          <div class="name_block">
            <div class="name">{{ data.name }}</div>
            <div class="slogan">{{ data.slogan }}</div>
          </div>
          <div class="data_block">
            <div class="data_detail">
              <div class="data_item">
                <div>{{ data.jobs.length }}个</div>
                <div class="title">职位招聘</div>
              </div>
              <div class="bottom_line"></div>
              <div class="data_item">
                <div>{{ data.size }}</div>
                <div class="title">公司规模</div>
              </div>
              <div class="bottom_line"></div>
              <div class="data_tags">
                <div>
                  <span v-for="item in companyTags" :key="item">{{
                    item
                  }}</span>
                </div>
              </div>
              <div class="bottom_line"></div>
              <div class="data_item">
                <el-link :href="data.website" target="_blank">{{
                  data.website
                }}</el-link>
                <div class="title">公司官网</div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-row class="content_block">
        <el-col :span="24" class="block_title">公司简介</el-col>
        <el-col :span="24" class="description">
          <pre>{{ data.description }}</pre>
        </el-col>
      </el-row>
      <el-row v-if="data.jobs.length" class="content_block">
        <el-col :span="24" class="block_title">招聘职位</el-col>
        <el-col v-for="item in data.jobs" :key="item.id" :span="24">
          <a :href="getJobURL(item)" target="_blank" class="job_link">
            <el-card class="job_item" shadow="hover">
              <div class="job_main">
                <div>
                  <div class="job_title">
                    {{ item.title }}
                  </div>
                  <div class="job_time">发布于：{{ displayTime(item) }}</div>
                </div>
                <div class="job_salary">
                  {{ displaySalary(item) }}
                </div>
              </div>
            </el-card>
          </a>
        </el-col>
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
.image {
  width: 100%;
  height: 100%;
}

.info_block {
  height: 200px;
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
}

.content_block {
  margin-top: 20px;
  background-color: rgb(250, 250, 250);
  border: 1px solid rgb(237, 237, 237);
  padding: 20px;
}
.job_link {
  text-decoration: none;
}
.job_item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
}

.job_main {
  display: flex;
  justify-content: space-between;
}
.job_title {
  font-size: 1.1rem;
  font-weight: bold;
  color: var(--theme-primary-color);
}
.job_salary {
  font-size: 1.5rem;
  color: #e31117;
  font-weight: 700;
}
.description {
  margin-top: 10px;
}

.block_title {
  font-size: 1.3rem;
  font-weight: bold;
  color: var(--theme-primary-color);
}

.info_line {
  display: flex;
  flex-direction: column;
}
.bottom_line {
  top: 0;
  right: 0;
  width: 1px;
  background: #d0d0d0;
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
.data_item {
  margin-left: 10px;
  text-align: center;
  margin-right: 10px;
  width: 120px;
}

.data_tags span {
  margin-left: 5px;
  margin-right: 5px;
  border: 1px solid #a6a6a6;
  border-radius: 3px;
  padding: 0 5px;
}

.data_tags {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 20px;
  margin-right: 20px;
}

.title {
  font-size: 0.9rem;
  color: #929292;
}

.data_block {
  position: relative;
  bottom: 0;
  height: 30%;
  background-color: #f1f1f1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.data_detail {
  display: flex;
}
.name_block {
  flex-grow: 1;
  margin-left: 20px;
  padding-top: 20px;
}

.name {
  color: var(--theme-primary-color);
  font-size: 1.5rem;
  font-weight: bold;
}
.failure {
  text-align: center;
  margin-top: 250px;
  color: var(--theme-primary-color);
  font-weight: bolder;
}

pre {
  white-space: pre-line;
  font-size: 1rem;
}
</style>