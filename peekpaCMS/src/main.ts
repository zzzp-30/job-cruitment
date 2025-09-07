import { createApp } from 'vue'
import './style.css'
import * as ElIcons from '@element-plus/icons-vue';
import App from './App.vue'
import store from './store';
import router from './route';
import 'element-plus/theme-chalk/index.css';

const app = createApp(App);
app.use(store);
app.use(router);  // 挂载路由
// 全局注册element-plus icon图标组件
Object.keys(ElIcons).forEach((key) => {
  app.component(`Eli${key}`, ElIcons[key as keyof typeof ElIcons]);
});
app.mount('#app');