<script setup lang="ts">
import {type Filter } from '../types/base';

// 定义组件props
const props = defineProps<{
  dataList: Filter[] | []; // 分类标签列表
}>();

// 定义组件emit
const emit = defineEmits<{
  // 将标签点击数据提交给父组件处理
  (eventName: 'searchKey', param: string, value: string): void;
}>();
</script>

<template>
  <div class="category">
    <div v-for="item in props.dataList" :key="item.title" class="category_box">
      <div class="category_list">
        <div class="title">{{ item.title }}</div>
        <a
          v-for="subitem in item.filters"
          :key="subitem.name"
          :href="subitem.param"
          target="_blank"
          @click.prevent="emit('searchKey', item.param, subitem.param)"
          ><div>{{ subitem.name }}</div></a
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.category {
  float: left;
  position: relative;
  width: 452px;
}

.category_box {
  position: relative;
  padding: 9px 0;
}

.category_list {
  position: relative;
  height: 20px;
  line-height: 20px;
  overflow: hidden;
  border-right: 0;
}

.title {
  display: inline-block;
  margin: 0;
  font-size: 16px;
  font-family: PingFangSC-Medium, PingFang SC;
  font-weight: 600;
  color: #333;
}
.title::after {
  content: '|';
  margin: 0 10px;
  width: 1px;
  height: 16px;
  color: #e8e9eb;
}

.category_list a {
  padding-right: 20px;
  white-space: nowrap;
  text-decoration: none;
  outline: none;
  cursor: pointer;
  transition: color 0.3s;
  color: #666;
}

.category_list a:hover {
  color: var(--theme-color);
  text-decoration: underline;
}
.category_list a div {
  margin: 0;
  display: inline;
  font-size: 14px;
  font-family: PingFangSC-Regular, PingFang SC;
  font-weight: 400;
}
</style>