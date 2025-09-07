<script setup lang="ts">
// 刷新页面
const reload = () => {
  window.location.reload();
};
</script>

<template>
  <div class="loading_container" @click="reload">页面加载失败，点击重试</div>
</template>

<style scoped>
.loading_container {
  color: var(--theme-primary-color);
  text-align: center;
  display: flex;
  font-weight: bold;
  justify-content: center;
  cursor: pointer;
}
</style>