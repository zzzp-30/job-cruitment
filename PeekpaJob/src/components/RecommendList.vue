<script setup lang="ts">
import { computed, ref } from 'vue';
import CompanyCard from './CompanyCard.vue';
import JobIndexCard from './JobIndexCard.vue';
import type { Job } from '../types/Job';
import type { Company } from '../types/Company';
import { type RecommendList, RecommendType } from '../types/base';

// 定义组件props
const props = defineProps<{
  dataList: RecommendList<Job | Company>[]; // 推荐数据列表
  type: RecommendType; // 推荐数据类型
}>();

// 当前高亮标签index
const currentIndex = ref<number>(0);

// 计算属性，将推荐数据转化成职位推荐列表
const dataList = computed((): (Job | Company)[] => {
  if (props.dataList && props.dataList.length) {
    if (props.type === RecommendType.JOB) {
      return props.dataList[currentIndex.value].data_list as Job[];
    } 
    if (props.type === RecommendType.COMPANY) {
      return props.dataList[currentIndex.value].data_list as Company[];
    }
  }
  return [];
});

</script>

<template>
  <div v-if="props.dataList.length">
    <ul class="recomment_tabbar">
      <li
        v-for="(item, index) in props.dataList"
        :key="item.name"
        class="recommendTab"
        :class="{ current: currentIndex == index }"
        @click="currentIndex = index"
      >
        {{ item.name }}
      </li>
    </ul>

    <div v-if="props.type === RecommendType.JOB" class="recomment_list">
      <el-row :gutter="20">
        <JobIndexCard
          v-for="subitem in dataList"
          :key="subitem.id"
          :item="(subitem as Job)"
        />
      </el-row>
    </div>
    <div v-if="props.type === RecommendType.COMPANY" class="recomment_list">
      <el-row :gutter="20">
        <CompanyCard
          v-for="subitem in dataList"
          :key="subitem.id"
          :item="(subitem as Company)"
        />
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.recomment_list {
  list-style: none;
  padding: 0 0 10px 0;
}

.recomment_tabbar {
  position: relative;
  margin-top: 40px;
  margin-bottom: 14px;
  font-size: 0;
  border-bottom: 1px solid #e8e8e8;
  padding: 0;
}

.recomment_tabbar li {
  display: inline-block;
  padding: 14px 0;
  margin-right: 58px;
  font-size: 16px;
  color: #999;
  cursor: pointer;
}

.recomment_tabbar li.current {
  border-bottom: 2px solid #333;
  background: #fff;
  color: #333;
}
</style>