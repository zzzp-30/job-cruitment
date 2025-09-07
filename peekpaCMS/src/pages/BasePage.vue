<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { onMounted } from 'vue';
import useStore from '../store/modules/User';
import { useRouter } from 'vue-router';
import ROUTER_CONSTANTS from '../route/constants';
import vHeader from '../components/HeaderComponent.vue';
import vSidebar from '../components/SidebarComponent.vue';

// User store
const userStore = useStore();
const router = useRouter();

// 第一次进入页面，判断用户是否已经登录，如果未登录则跳转到登录页面
onMounted(() => {
  if (!userStore.isLogin()) {
    ElMessage.error('请先登录');
    router.push({
      name: ROUTER_CONSTANTS.LOGIN,
    });
  }
});

</script>

<template>
  <v-header />
  <v-sidebar />
  <div class="content-box">
    <div class="content">
      <router-view v-slot="{ Component }">
        <transition name="move" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<style scope>
.content-box {
  position: absolute;
  left: 250px;
  right: 0;
  top: 70px;
  bottom: 0;
  -webkit-transition: left 0.3s ease-in-out;
  transition: left 0.3s ease-in-out;
  background: #f0f0f0;
}

.content {
  width: auto;
  height: 100%;
  padding: 10px;
  overflow-y: scroll;
  box-sizing: border-box;
}
</style>