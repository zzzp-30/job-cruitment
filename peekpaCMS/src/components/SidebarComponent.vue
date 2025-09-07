<script lang="ts" setup>
import { computed, ref, resolveComponent, watch } from 'vue';
import { useRoute } from 'vue-router';
import PEEKPA_PERMISSION from '../store/modules/PermissionConstants';
import useStore from '../store/modules/User';
// 全局路由
const route = useRoute();
const userStore = useStore();
// 导航菜单选项接口
interface NavItem {
  icon?: string;
  path: string;
  title: string;
  subgroup?: NavItem[];
  permission?: string;
}
// 导航菜单栏数据列表
const navList: NavItem[] = [
  {
    icon: 'eli-Odometer',
    path: '/dashboard',
    title: '首页',
  },
  {
    icon: 'eli-Document',
    path: '/job',
    title: '职位管理',
    subgroup: [
      {
        path: '/publish',
        title: '发布职位',
      },
      {
        path: '/manage',
        title: '职位管理',
      },
    ],
  },
  {
    icon: 'eli-VideoCamera',
    path: '/interview/manage',
    title: '面试管理',
  },
  {
    icon: 'eli-User',
    path: '/user/manage',
    title: '员工管理',
    permission: PEEKPA_PERMISSION.MANAGER,
  },
  {
    icon: 'eli-Setting',
    path: '/setting',
    title: '修改资料',
  },
];

const superuserNavList: NavItem[] = [
  {
    icon: 'eli-house',
    path: '/company/manage',
    title: '公司管理',
  },
];

const resolveIcon = (componentName: string) => {
  const resolvedComponent = resolveComponent(componentName);
  return resolvedComponent;
};

const navItems = ref<NavItem[]>([]);


// 默认激活菜单的 index
const onRoutes = computed(() => {
  return route.path;
});

watch(
  () => userStore.token,
  (newValue) => {
    if (!newValue) {
      navItems.value = [];
    } else if (userStore.getUser?.is_superuser) {
      navItems.value = superuserNavList;
    } else {
      navList.forEach((item: NavItem) => {
        if (item.permission) {
          const userPerm = userStore.getUser;
          if (userPerm && userPerm.is_manager) {
            const tmp: NavItem = {
              icon: item.icon,
              path: item.path,
              title: item.title,
              subgroup: item.subgroup,
            };
            navItems.value.push(tmp);
          }
        } else {
          navItems.value.push(item);
        }
      });
    }
  },
  { immediate: true, deep: true }
);
</script>

<template>
  <div class="sidebar">
    <el-menu
      class="sidebar-el-menu"
      :default-active="onRoutes"
      background-color="var(--theme-one-color)"
      text-color="var(--theme-four-color)"
      active-text-color="var(--theme-three-color)"
      unique-opened
      router
    >
      <template v-for="item in navItems" :key="item.path">
        <el-sub-menu v-if="item.subgroup" :index="item.path">
          <template #title
            ><el-icon v-if="item.icon">
              <component :is="resolveIcon(item.icon)" /></el-icon
            >{{ item.title }}</template
          >

          <el-menu-item-group v-if="item.subgroup">
            <el-menu-item
              v-for="sub in item.subgroup"
              :key="sub.path"
              :index="`${item.path}${sub.path}`"
              >{{ sub.title }}</el-menu-item
            >
          </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item v-else :index="item.path">
          <el-icon v-if="item.icon">
            <component :is="resolveIcon(item.icon)"
          /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </template>
    </el-menu>
  </div>
</template>


<style scoped>
.sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
  width: 0;
}
.sidebar-el-menu:not(.el-menu--collapse) {
  width: 250px;
}
.sidebar > ul {
  height: 100%;
}

.el-menu-item {
  --el-menu-hover-bg-color: var(--theme-two-color);
}
.el-menu-item.is-active {
  background-color: var(--el-menu-hover-bg-color);
}
</style>