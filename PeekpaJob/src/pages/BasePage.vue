<script setup lang="ts">
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
</script>

<template>
  <el-container class="peekpa_container">
    <el-header class="peekpa_base_index"
      ><HeaderComponent></HeaderComponent
    ></el-header>
    <el-main class="peekpa_main">
      <router-view></router-view>
    </el-main>
    <el-footer class="peekpa_footer"
      ><FooterComponent></FooterComponent
    ></el-footer>
  </el-container>
</template>


<style scoped>
.peekpa_container {
  height: 100%;
}

.peekpa_main {
  width: var(--main-width);
  margin: 60px auto 0 auto;
  padding-left: 0;
  padding-right: 0;
  overflow: visible;
}
.peekpa_base_index {
  padding: 0;
  width: 100%;
  position: fixed;
  z-index: 999;
}

.peekpa_footer {
  padding: 0;
  height: 170px;
}
</style>