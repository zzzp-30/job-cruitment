import  { createRouter, createWebHashHistory } from 'vue-router';
import  type {  RouteRecordRaw } from 'vue-router';
import  ROUTER_CONSTANTS from './constants';

import PEEKPA_PERMISSION from '../store/modules/PermissionConstants';

const LoginPage = () => import('../pages/user/LoginPage.vue');
const BasePage = () => import('../pages/BasePage.vue');
const CMSBasePage = () => import('../pages/CMSBasePage.vue');
const NotfoundPage = () => import('../pages/exception/NotFoundPage.vue');


const routes: RouteRecordRaw[] = [
    // 登录页面
    {
      path: '/login',
      name: ROUTER_CONSTANTS.LOGIN,
      component: LoginPage,
    },
    {
      path: '/',
      name: 'Home',
      component: BasePage,
      redirect: 'dashboard',
      children: [
        {
          path: 'dashboard',
          name: ROUTER_CONSTANTS.CMS_DASHBOARD,
          component: CMSBasePage,
          props: {
            page: ROUTER_CONSTANTS.CMS_DASHBOARD,
          },
        },
        {
          path: 'job',
          children: [
            {
              path: 'publish',
              name: ROUTER_CONSTANTS.CMS_JOB_PUBLISH,
              component: CMSBasePage,
              props: {
                page: ROUTER_CONSTANTS.CMS_JOB_PUBLISH,
              },
            },
            {
              path: 'manage',
              name: ROUTER_CONSTANTS.CMS_JOB_MANAGE,
              component: CMSBasePage,
              props: {
                page: ROUTER_CONSTANTS.CMS_JOB_MANAGE,
              },
            },
          ],
        },
        {
          path: 'interview/manage',
          name: ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE,
          component: CMSBasePage,
          props: {
            page: ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE,
          },
        },
        {
          path: 'user',
          children: [
            {
              path: 'manage',
              name: ROUTER_CONSTANTS.CMS_USER_MANAGE,
              component: CMSBasePage,
              props: {
                page: ROUTER_CONSTANTS.CMS_USER_MANAGE,
              },
            },
          ],
          meta: {
            requirePermission: [PEEKPA_PERMISSION.MANAGER],
          },
        },
        {
          path: 'company',
          children: [
            {
              path: 'manage',
              name: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
              component: CMSBasePage,
              props: {
                page: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
              },
            },
          ],
          meta: {
            requirePermission: [PEEKPA_PERMISSION.SUPERUSER],
          },
        },
        {
          path: 'setting',
          name: ROUTER_CONSTANTS.CMS_SETTING,
          component: CMSBasePage,
          props: {
            page: ROUTER_CONSTANTS.CMS_SETTING,
          },
        },
      ],
    },
    // 404 页面
    {
      path: '/:pathMatch(.*)*',
      name: ROUTER_CONSTANTS.NOTFOUND_404,
      component: NotfoundPage,
      meta: {
        title: '网页未找到 PeekpaCom',
      },
    },
];
// 创建 Hash 模式路由对象
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 导出路由对象
export default router;

