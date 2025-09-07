<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { type LocationQuery, useRoute, useRouter } from 'vue-router';
import SearchComponent from '../../components/SearchComponent.vue';
import FilterComponent from '../../components/FilterComponent.vue';
import { type Filter } from '../../types/base';
import { joblistFilters, joblistOrder } from '../../constants/filter';
import { type JobListResponse } from '../../types/Job';
import { getJobList } from '../../services/job';
import JobCard from '../../components/JobCard.vue';
import ROUTER_CONSTANTS from '../../route/constants';

const LIMIT = 10;
let curOffset = 0;

// 搜索框内容
const initSearchKey = ref<string>('');
const data = ref<JobListResponse>();
const router = useRouter();
const route = useRoute();
const filterData = ref<Filter[]>(joblistFilters);
const filterOrder = ref<Filter[]>(joblistOrder);
const loading = ref<boolean>(true);
const curPage = ref<number>(1);
const total = ref<number>(0);

// 处理搜索，过滤器点击事件。原理就是将搜索参数通过路由传递给
// 列表页面，然后列表页面渲染时根据参数搜索。
const search = async (param: string, value: string) => {
  const currentQuery = { ...route.query };
  if (value === '' && currentQuery[param]) {
    delete currentQuery[param];
  } else {
    currentQuery[param] = value;
  }
  await router.push({
    name: ROUTER_CONSTANTS.JOB_LIST,
    query: currentQuery,
  });
};

// 请求数据
const requestData = async (offset: number, query: LocationQuery) => {
  try {
    loading.value = true;
    initSearchKey.value = '';
    const response = await getJobList(LIMIT, offset, query);
    if (response.status === 200) {
      data.value = response.data;
      total.value = response.data.count;
      curPage.value = curOffset / LIMIT + 1;
      if (query.q) {
        initSearchKey.value = query.q as string;
      }
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
  requestData(0, route.query);
});

// 处理页面跳转
const handlePageChange = async (value: number) => {
  curOffset = (value - 1) * LIMIT;
  await requestData(curOffset, route.query);
};
</script>

<template>
  <div class="index_container">
    <SearchComponent :init-key="initSearchKey" @search-key="search" />
    <div v-if="data" class="list_container">
      <FilterComponent
        :data-list="filterData"
        :query="route.query"
        @search="search"
      />

      <FilterComponent
        :data-list="filterOrder"
        :query="route.query"
        @search="search"
      />
      <JobCard v-for="item in data.results" :key="item.id" :item="item" />
      <el-pagination
        class="pagination"
        background
        layout="prev, pager, next"
        :current-page="curPage"
        :total="total"
        :page-size="LIMIT"
        @current-change="handlePageChange"
      ></el-pagination>
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
.list_container {
  margin: 100px auto 0 auto;
  width: 1200px;
}

.pagination {
  margin: 20px auto 0 auto;
}
.failure {
  text-align: center;
  margin-top: 250px;
  color: var(--theme-primary-color);
  font-weight: bolder;
}
</style>