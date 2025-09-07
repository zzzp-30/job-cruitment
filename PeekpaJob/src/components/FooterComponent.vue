<script setup lang="ts">
import { ref } from 'vue';

const year = ref<number>(2023);
year.value = new Date().getFullYear();
</script>

<template>
  <div class="footer_container">
    <ul class="footer_list">
      <li class="footer_li">
        <div class="logo"></div>
      </li>
      <li class="footer_li">
        <div>
          © {{ year }} Copyright:
          <a href="https://peekpa.com" target="_blank">peekpa.com</a>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.footer_container {
  height: 170px;
  width: 100%;
  min-width: 1250px;
  border-top: 1px solid #e8e8e8;
  background: #fafafa;
  background-color: var(--theme-primary-color);
  width: 100%;
  height: 150px;
  text-align: center;
  clear: both;
  margin-top: 20px;
  position: relative;
  z-index: 110;
}

.footer_list {
  display: inline-block;
  width: 1200px;
  margin: 0 auto;
  padding-top: 40px;
  list-style: none;
}

.footer_list li {
  float: left;
  width: 100%;
  font-size: 14px;
  color: var(--theme-third-color);
  text-align: center;
}

.footer_li + .footer_li {
  margin-top: 16px;
}

.logo {
  margin: 0 auto;
  width: 135px;
  height: 50px;
  background: url('../../assets/logo-black.png');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>