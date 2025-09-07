<script setup lang="ts">
import { computed } from 'vue';
import type { Job } from '../types/Job';

// 定义组件props
const props = defineProps<{
  item: Job; // 职位卡片数据
}>();

// 计算属性，显示职位薪水
const displaySalary = computed(() => {
  const max = Number((props.item.salary_max / 1000).toFixed(1));
  const min = Number((props.item.salary_min / 1000).toFixed(1));
  if (max === min) {
    return `${max}K`;
  }
  return `${min}K~${max}K`;
});

// 格式化显示发布时间
const displayTime = computed(() => {
  const date: Date = new Date(props.item.publish_time);
  const year: number = date.getFullYear();
  const month: string = String(date.getMonth() + 1).padStart(2, '0');
  const day: string = String(date.getDate()).padStart(2, '0');
  const hours: string = String(date.getHours()).padStart(2, '0');
  const minutes: string = String(date.getMinutes()).padStart(2, '0');
  return `${year}年${month}月${day}日 ${hours}点${minutes}分`;
});

// 计算属性，显示公司标签
const displayCompanyTags = computed(() => {
  return props.item.company_tags.replace(new RegExp(',', 'g'), ' / ');
});

// 计算职位详情地址
const getJobUrl = computed(() => {
  const baseUrl = import .meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/#/job/${props.item.id}/`;
});

// 计算公司详情地址
const getCompanyUrl = computed(() => {
  const baseUrl = import .meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/#/company/${props.item.company_id}/`;
});

// 计算公司图片地址
const getCompanyAvatar = computed(() => {
  const baseUrl = import .meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/${props.item.company_avatar}`;
});
</script>

<template>
  <el-card shadow="hover" :body-style="{ padding: '0px' }" class="card">
    <el-row class="first_row">
      <el-col :span="12" class="vertical_center">
        <div>
          <el-link class="title" :href="getJobUrl" target="_blank">{{
            item.title
          }}</el-link>
          <span class="location"
            ><el-icon :size="13"><eli-Location /></el-icon>{{ item.city }}</span
          >
        </div>

        <div class="salary">
          {{ displaySalary }}
          <span class="experience"
            >{{ item.experience }} / {{ item.education }}</span
          >
        </div>
      </el-col>
      <el-col :span="6" class="vertical_center">
        <div>
          <el-link class="company_name" :href="getCompanyUrl" target="_blank">
            {{ item.company_name }}</el-link
          >
        </div>
        <div>{{ displayCompanyTags }}</div></el-col
      >
      <el-col :span="6">
        <el-image class="image" :src="getCompanyAvatar" fit="fill"
          ><template #placeholder>
            <div class="image-slot">Loading<span class="dot">...</span></div>
          </template></el-image
        ></el-col
      >
    </el-row>
    <el-row class="second_row">
      <el-col :span="12">发布于: {{ displayTime }}</el-col>
      <el-col :span="12">"{{ item.benefit }}"</el-col>
    </el-row>
  </el-card>
</template>

<style scoped>
.card {
  margin-top: 20px;
}
.first_row {
  padding: 15px 20px 15px 20px;
}
.second_row {
  padding: 15px 20px 15px 20px;
  background-color: rgb(250, 250, 250);
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

.title {
  color: var(--theme-primary-color);
  font-size: 1.3rem;
  font-weight: bold;
}
.company_name {
  font-weight: bold;
  color: var(--theme-primary-color);
}

.vertical_center {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.location {
  margin-left: 10px;
  font-size: 1.1rem;
  font-weight: normal;
  color: var(--theme-secondary-color);
}

.salary {
  color: #e31117;
  font-weight: 700;
}
.experience {
  color: #545454;
  font-weight: normal;
}

.image {
  height: 60px;
  width: 60px;
}
</style>