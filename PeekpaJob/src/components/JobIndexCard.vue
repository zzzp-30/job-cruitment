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

// 显示公司标签
const companyTags = computed(() => {
  return props.item.company_tags.split(',');
});

// 获取职位 URL
const getJobUrl = computed(() => {
  return `http://localhost:8001/#/job/${props.item.id}/`;
});
</script>

<template>
  <el-col :span="8">
    <el-card shadow="hover" :body-style="{ padding: '0px' }" class="card">
      <el-row class="row">
        <el-col :span="16"
          ><el-link class="title" :href="getJobUrl" target="_blank">{{
            item.title
          }}</el-link></el-col
        >
        <el-col :span="8" class="text_right salary">{{ displaySalary }}</el-col>
      </el-row>
      <el-row class="row">
        <el-col :span="16">{{ item.experience }} / {{ item.education }}</el-col>
        <el-col :span="8" class="text_right">{{ item.company_name }}</el-col>
      </el-row>
      <el-row class="row">
        <el-col :span="18" class="tag_list">
          <span v-for="label in companyTags" :key="label" :title="label">{{
            label
          }}</span>
        </el-col>
        <el-col :span="6" class="text_right">{{ item.city }}</el-col>
      </el-row>
    </el-card>
  </el-col>
</template>

<style scoped>
.card {
  margin-top: 20px;
  padding: 10px;
}
.title {
  font-size: 1.1rem;
  color: var(--theme-primary-color);
}

.text_right {
  text-align: right;
}

.salary {
  color: #e31117;
}

.tag_list span {
  display: inline-block;
  padding: 0 8px;
  font-size: 0.8rem;
  line-height: 26px;
  color: #999;
  border: 1px solid #f0f0f0;
  border-radius: 3px;
  text-align: center;
}
.tag_list span + span {
  margin-left: 6px;
}

.row {
  margin: 8px 0;
}
</style>