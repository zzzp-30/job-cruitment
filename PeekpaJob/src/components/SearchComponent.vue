<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

// 定义组件props
const props = defineProps<{
  initKey?: string; // 搜索内容关键字初始值，可选
}>();

// 定义组件emit
const emit = defineEmits<{
  // 将搜索的点击事件交由父组件处理
  (eventName: 'searchKey', param: string, value: string): void;
}>();

// 当前页面路由
const route = useRoute();

// 搜索框内的关键字
const keyWord = ref<string>('');

// 监听路由的path变化，当path变化，意味着切换页面，要情况搜索框内容
watch(
  () => route.path,
  () => {
    keyWord.value = '';
  }
);

// 监听搜索内容初始值，如果有值，则赋值与搜索框内
watch(
  () => props.initKey,
  (newValue) => {
    keyWord.value = newValue as string;
  },
  { immediate: true }
);
</script>

<template>
  <div class="search">
    <div class="search_container">
      <form action="#" class="search-form">
        <input v-model="keyWord" type="text" class="search_input" />
        <input
          type="submit"
          value="搜索"
          class="search_button"
          @click.prevent="emit('searchKey', 'q', keyWord)"
        />
      </form>
    </div>
  </div>
</template>

<style scoped>
.search {
  background: rgb(242, 245, 244);
  position: fixed;
  width: 100%;
  top: 60px;
  left: 0px;
  z-index: 110;
  padding: 20px 0;
}

.search_container {
  width: 1200px;
  height: 46px;
  margin: 0 auto;
  position: relative;
}

.search_input {
  width: 762px;
  height: 46px;
  line-height: 46px;
  float: left;
  font-size: 16px;
  padding: 0 16px;
  margin: 0;
  border: 1px solid #e8e8e8;
  border-right: 0;
}

.search_input:focus {
  border: 1px solid var(--theme-primary-color);
  outline: none !important;
  color: var(--theme-color);
}
.search_button {
  float: left;
  width: 142px;
  height: 46px;
  font-size: 18px;
  color: #fff;
  border: 0;
  background: var(--theme-primary-color);
  cursor: pointer;
}
</style>