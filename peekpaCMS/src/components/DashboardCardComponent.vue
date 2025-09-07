<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title: string;
    count: number;
    icon: string;
  }>(),
  {
    title: '标题',
    count: 0,
    icon: 'eli-ChromeFilled',
  }
);
</script>

<template>
  <div class="small-box card">
    <div class="inner">
      <h2>{{ props.count }}</h2>
      <p>{{ props.title }}</p>
    </div>
    <el-icon class="icon"><component :is="props.icon"> </component></el-icon>
  </div>
</template>

<style scoped>
.small-box {
  height: 100px;
  box-sizing: border-box;
  position: relative;
  background: radial-gradient(
    ellipse at center,
    var(--theme-two-color) 0%,
    var(--theme-one-color) 70%
  );
  background-size: 100%;
  color: var(--theme-three-color);
  text-shadow: 0 0 20px var(--theme-four-color), 0 0 20px var(--theme-one-color);
  border-radius: 4px;
}
.inner {
  padding: 10px;
}
.inner p {
  padding-top: 10px;
}

.inner h2 {
  color: var(--theme-four-color);
  padding-top: 5px;
}

.small-box:hover .icon {
  font-size: 55px;
}

.icon {
  font-size: 45px;
  position: absolute;
  right: 10px;
  top: 10px;
  transition: all 0.2s linear;
}
</style>