<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import HeaderUserInfoComponent from './HeaderUserInfoComponent.vue';

interface NavMenu {
  name: string; // 导航显示名称
  url: string; // 导航跳转URL
}

const BasicNavList: NavMenu[] = [
  {
    name: '首页',
    url: '/',
  },
  {
    name: '职位',
    url: '/jobs',
  },
  {
    name: '公司',
    url: '/companies',
  },
];

// 当前高亮导航的index
const currentIndex = ref<number>(-1);
// 当前页面Route
const route = useRoute();

// 根据路由地址变化更新高亮路由index
const updateIndex = () => {
  const currentItemIndex = BasicNavList.findIndex(
    (item: NavMenu) => route.path === item.url
  );
  if (route.path.indexOf('job') !== -1) {
    currentIndex.value = 1;
  } else if (route.path.indexOf('compan') !== -1) {
    currentIndex.value = 2;
  } else {
    currentIndex.value = -1;
  }
  currentIndex.value =
    currentItemIndex === -1 ? currentIndex.value : currentItemIndex;
};

// 主要负责第一次进入页面，找到当前导航按钮，更新当前高亮导航index值
onMounted(() => {
  updateIndex();
});

// 监听路由变化，更新高亮路由index
watch(
  () => route,
  () => {
    updateIndex();
  },
  { deep: true }
);
</script>

<template>
  <div class="header">
    <div class="inner">
      <div class="float_left">
        <a href="#" class="logo"></a>
        <ul class="left_ul">
          <div
            v-for="(item, index) in BasicNavList"
            :key="item.name"
            class="nav_container"
          >
            <router-link
              class="nav"
              :class="{
                tab_active: index === currentIndex,
              }"
              :to="item.url"
              @click="currentIndex = index"
              >{{ item.name }}</router-link
            >
          </div>
        </ul>
      </div>
      <div>
        <HeaderUserInfoComponent></HeaderUserInfoComponent>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  z-index: 120;
  width: 100%;
  height: 100%;
  background-color: var(--theme-primary-color);
  color: white;
  top: var(--vt-banner-height);
  box-shadow: var(--el-box-shadow);
}

.inner {
  width: var(--main-width);
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: 0 auto;
  cursor: default;
}

.float_left {
  display: flex;
}

ul {
  margin: 0;
}

.header .logo {
  text-decoration: none;
  margin: auto;
  width: 135px;
  height: 50px;
  background-image: url('../../assets/logo-white.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
}

.left_ul {
  margin-left: 20px;
  list-style: none;
  font-size: var(--el-font-size-extra-large);
}

.left_ul .nav {
  padding: 16px 20px;
  outline: none;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s;
  color: var(--theme-secondary-color);
  line-height: 60px;
  height: 60px;
}
.nav_container {
  display: inline;
}

.left_ul .tab_active {
  color: var(--theme-primary-color);
}

.left_ul .nav:hover {
  color: var(--theme-third-color);
}

.left_ul .tab_active:hover {
  color: var(--theme-secondary-color);
}

.tab_active {
  background: var(--theme-third-color);
  cursor: default;
  font-weight: bold;
}
</style>