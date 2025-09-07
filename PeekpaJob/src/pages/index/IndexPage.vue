<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import SearchComponent from '../../components/SearchComponent.vue';
import CategoryComponent from '../../components/CategoryComponent.vue';
import BannerComponent from '../../components/BannerComponent.vue';
import RecommendList from '../../components/RecommendList.vue';
import { getIndexData } from '../../services/common';
import type { IndexResponse } from '../../types/Common';
import { RecommendType } from '../../types/base';
import ROUTER_CONSTANTS from '../../route/constants';

// 搜索框内容
const initSearchKey = ref<string>('');
const data = ref<IndexResponse>();
const router = useRouter();
const route = useRoute();
const loading = ref<boolean>(true);

// 处理搜索，过滤器点击事件。原理就是将搜索参数通过路由传递给
// 列表页面，然后列表页面渲染时根据参数搜索。
const search = async (param: string, value: string) => {
  const currentQuery = { ...route.query };
  if (value === '' && currentQuery[param]) {
    delete currentQuery[param];
  } else {
    currentQuery[param] = value;
  }
  router.push({
    name: ROUTER_CONSTANTS.JOB_LIST,
    query: currentQuery,
  });
};

// 请求数据
const requestData = async () => {
  try {
    // 数据复位
    loading.value = true;
    const response = await getIndexData();
    if (response.status === 200) {
      data.value = response.data;
    }
    loading.value = false;
    window.scrollTo(0, 0);
  } catch (error) {
    // 这里可以自定义网络请求错误处理
    ElMessage.error(`网络请求失败`);
    loading.value = false;
  }
};

onMounted(() => {
  requestData();
});
</script>

<template>
  <div class="index_container">
    <SearchComponent :init-key="initSearchKey" @search-key="search" />
    <div v-if="data" class="info_container">
      <el-row :gutter="20">
        <el-col :span="8">
          <CategoryComponent :data-list="data.category" @search-key="search" />
        </el-col>
        <el-col :span="16">
          <BannerComponent :data-list="data.banner" />
        </el-col>
      </el-row>
      <RecommendList :data-list="data.recommend_jobs" :type="RecommendType.JOB" />
      <RecommendList
        :data-list="data.recommend_companies"
        :type="RecommendType.COMPANY"
      />
    </div>
    <div v-else-if="!loading && !data" class="failure">
      没有数据，请稍后再试
    </div>
  </div>
</template>

<style scoped>
.failure {
  text-align: center;
  margin-top: 250px;
  color: var(--theme-primary-color);
  font-weight: bolder;
}
.index_container {
  min-height: calc(100vh - 170px - 60px - 40px);
}
.info_container {
  margin-top: 98px;
}
</style>