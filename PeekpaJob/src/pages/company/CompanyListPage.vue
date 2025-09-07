<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { type LocationQuery, useRoute, useRouter } from 'vue-router';
import SearchComponent from '../../components/SearchComponent.vue';
import FilterComponent from '../../components/FilterComponent.vue';
import CompanyCard from '../../components/CompanyCard.vue';
import { type Filter } from '../../types/base';
import {
  companylistFilters,
  companylistOrder,
} from '../../constants/filter';
import { type CompanyListResponse } from '../../types/Company';
import { getCompanyList } from '../../services/company';
import ROUTER_CONSTANTS from '../../route/constants';

const LIMIT = 12;
let curOffset = 0;
const initSearchKey = ref<string>('');
const router = useRouter();
const route = useRoute();
const data = ref<CompanyListResponse>();
const filterData = ref<Filter[]>(companylistFilters);
const filterOrder = ref<Filter[]>(companylistOrder);
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
  router.push({
    name: ROUTER_CONSTANTS.COMPANY_LIST,
    query: currentQuery,
  });
};

// 请求数据
const requestData = async (offset: number, query: LocationQuery) => {
  try {
    // 数据复位
    loading.value = true;
    initSearchKey.value = '';
    // 请求数据
    const response = await getCompanyList(LIMIT, offset, query);
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

// 页面跳转逻辑
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
      <el-row :gutter="20">
        <CompanyCard v-for="item in data.results" :key="item.id" :item="item" />
      </el-row>
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