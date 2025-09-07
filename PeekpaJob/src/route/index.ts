import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router';
import ROUTER_CONSTANTS from './constants';

const IndexBasePage = () => import('../pages/IndexBasePage.vue');
const BasePage = () => import('../pages/BasePage.vue');
const NotFoundPage = () => import('../pages/exception/NotFoundPage.vue');

const routes: RouteRecordRaw[] = [
    {
    path: '/',
    component: BasePage,
    children: [
      {
        path: '',
        name: ROUTER_CONSTANTS.INDEX,
        component: IndexBasePage,
      },
      {
        path: 'jobs',
        name: ROUTER_CONSTANTS.JOB_LIST,
        component: IndexBasePage,
      },
      {
        path: 'job/:jobId',
        name: ROUTER_CONSTANTS.JOB_DETAIL,
        component: IndexBasePage,
      },
      {
        path: 'companies',
        name: ROUTER_CONSTANTS.COMPANY_LIST,
        component: IndexBasePage,
      },
      {
        path: 'company/:companyId',
        name: ROUTER_CONSTANTS.COMPANY_DETAIL,
        component: IndexBasePage,
      },
      {
        path: 'profile',
        name: ROUTER_CONSTANTS.PROFILE,
        component: IndexBasePage,
      },
      {
        path: 'signin',
        name: ROUTER_CONSTANTS.SIGN_IN,
        component: IndexBasePage,
      },
      {
        path: 'signup',
        name: ROUTER_CONSTANTS.SIGN_UP,
        component: IndexBasePage,
      },
      {
        path: '/:pathMatch(.*)*',
        name: ROUTER_CONSTANTS.NOTFOUND_404,
        component: NotFoundPage,
        meta: {
          title: '网页未找到 PeekpaJob',
        },
      },
    ],
  },
];

// 创建 Hash 模式路由对象
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 导出路由对象
export default router;