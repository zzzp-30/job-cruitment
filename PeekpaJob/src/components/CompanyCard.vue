<script setup lang="ts">
import { computed } from 'vue';
import { type Company } from '../types/Company';

// 定义组件props
const props = defineProps<{
  item: Company; // 职位卡片数据
}>();

// 格式化显示公司标签
const displayCompanyTags = computed(() => {
  return props.item.tags.replace(new RegExp(',', 'g'), '|');
});

// 公司详情地址
const getCompanyUrl = computed(() => {
  const baseUrl = import.meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/#/company/${props.item.id}/`;
});

// 公司头像地址
const getCompanyAvatar = computed(() => {
  const baseUrl = import.meta.env.VITE_COMPANY_SITE_URL;
  return `${baseUrl}/${props.item.avatar}`;
});
</script>

<template>
  <el-col :span="6">
    <el-card shadow="hover" :body-style="{ padding: '20px' }" class="card">
      <div class="first_line">
        <el-image class="image" :src="getCompanyAvatar" fit="fill"
          ><template #placeholder>
            <div class="image-slot">Loading<span class="dot">...</span></div>
          </template></el-image
        >
        <div>
          <el-link class="company_name" :href="getCompanyUrl" target="_blank">
            {{ item.name }}</el-link
          >
        </div>
        <div class="company_tag">{{ displayCompanyTags }}</div>
        <div class="company_slogan">{{ item.slogan }}</div>
      </div>
      <div class="second_line">
        <a :href="getCompanyUrl" target="_blank" class="bottom_item">
          <div>{{ item.jobs }}</div>
          <div class="bottom_text">招聘岗位</div>
        </a>
        <div class="bottom_line"></div>
        <a :href="getCompanyUrl" target="_blank" class="bottom_item">
          <div>{{ item.interviews }}</div>
          <div class="bottom_text">正在面试</div>
        </a>
      </div>
    </el-card>
  </el-col>
</template>

<style scoped>
.card {
  margin-top: 20px;
  width: 100%;
}

.first_line {
  text-align: center;
  border-bottom: 1px dashed rgb(224, 224, 224);
}

.second_line {
  display: flex;
  justify-content: space-around;
  text-align: center;
  margin-top: 10px;
}

.image {
  height: 80px;
  width: 80px;
}

.company_name {
  font-size: 1.1rem;
  font-weight: bold;
  color: var(--theme-primary-color);
}

.company_tag {
  min-height: 22px;
  margin: 5px 0;
  font-weight: 300;
  color: #6f6f6f;
}

.company_slogan {
  min-height: 22px;
  margin-bottom: 10px;
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

.bottom_line {
  top: 0;
  right: 0;
  width: 1px;
  background: #ededed;
}
.bottom_item {
  text-decoration: none;
  font-size: 1rem;
}
.bottom_text {
  color: #6f6f6f;
}
.bottom_text:hover {
  color: var(--theme-primary-color);
}
.bottom_item:hover {
  color: var(--theme-primary-color);
}
</style>