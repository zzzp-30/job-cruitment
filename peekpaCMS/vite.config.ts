import { defineConfig } from 'vite'
import type { PluginOption } from 'vite'
import vue from '@vitejs/plugin-vue'  // 使用命名导入
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
 base: '/cms/',  // 新添加 /cms/ 目录
 plugins: [
   vue() as PluginOption,
   AutoImport({
     resolvers: [ElementPlusResolver()],
   }),
   Components({
     resolvers: [ElementPlusResolver()],
   }),
 ],
 server: {
   host: "0.0.0.0",
   port: 8080
 },
})