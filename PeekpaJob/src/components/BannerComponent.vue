<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import type { Banner } from '../types/base';

// 轮播时间间隔，2秒
const SLIDE_TIME = 2000;

// 定义组件Props
const props = defineProps<{
  dataList: Banner[]; // 轮播图列表
}>();

// 当前页面index
const currentIndex = ref<number>(0);
// 轮播定时器
const timer = ref<number | null>();

// 计算属性，上一张轮播图index
const prevIndex = computed(() => {
  if (props.dataList) {
    if (currentIndex.value === 0) {
      return props.dataList.length - 1;
    }
    return currentIndex.value - 1;
  }
  return 0;
});

// 计算属性，下一张轮播图index
const nextIndex = computed(() => {
  if (props.dataList.length) {
    if (currentIndex.value === props.dataList.length - 1) {
      return 0;
    }
    return currentIndex.value + 1;
  }
  return 0;
});

// 开始轮播
const startSliding = () => {
  timer.value = setInterval(() => {
    currentIndex.value = nextIndex.value;
  }, SLIDE_TIME);
};

// 第一次进入页面开始自动轮播
onMounted(() => {
  startSliding();
});

// 当鼠标移动到图片时，停止轮播
const handleMouseover = () => {
  clearInterval(Number(timer.value));
};

// 当鼠标移动离开图片时，开始轮播
const handleMouseout = () => {
  startSliding();
};
</script>

<template>
  <div class="banner" @mouseover="handleMouseover" @mouseout="handleMouseout">
    <div v-if="props.dataList.length" class="item">
      <a
        :href="props.dataList[currentIndex].link_url"
        target="_blank"
        class="item"
        ><el-image
          class="item"
          :src="props.dataList[currentIndex].img_url"
          fit="fill"
          ><template #placeholder>
            <div class="image-slot">Loading<span class="dot">...</span></div>
          </template></el-image
        ></a
      >
    </div>
    <div class="control">
      <em class="left_arrow" @click="currentIndex = prevIndex"></em>
      <em class="right_arrow" @click="currentIndex = nextIndex"></em>
    </div>
  </div>
</template>

<style scoped>
ul li {
  list-style: none;
  float: left;
  width: 30px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}
.item {
  height: 100%;
  width: 100%;
}
.banner {
  position: relative;
  margin-top: 10px;
  height: 286px;
  overflow: hidden;
  background-color: #f2f5f4;
}
.banner img {
  width: 100%;
  display: block;
}
.banner .page {
  background: rgba(0, 0, 0, 0.5);
  position: absolute;
  right: 0;
  bottom: 0;
  width: 100%;
}
.banner .page ul {
  float: right;
}

.left_arrow {
  position: absolute;
  top: 126px;
  left: 20px;
  background-image: url('../../assets/banner_arrow_left.png');
  background-repeat: no-repeat;
  background-size: 18px 34px;
  width: 18px;
  height: 34px;
  cursor: pointer;
}

.right_arrow {
  position: absolute;
  right: 20px;
  top: 126px;
  background-image: url('../../assets/banner_arrow_right.png');
  background-repeat: no-repeat;
  background-size: 18px 34px;
  width: 18px;
  height: 34px;
  cursor: pointer;
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
</style>