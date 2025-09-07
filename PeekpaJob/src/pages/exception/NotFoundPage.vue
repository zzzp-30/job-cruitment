<script setup lang="ts"></script>

<template>
  <el-container class="peekpa_container">
    <el-main class="peekpa_main">
      <div class="center-xy">
        <p>404, 页面未找到.</p>
        <span class="handle blink"></span>
      </div>
    </el-main>
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

.center-xy {
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  position: absolute;
  padding: 0 20px;
}
p {
  font-size: 24px;
  letter-spacing: 0.2px;
  margin: 0;
  color: var(--theme-primary-color);
}
.handle {
  background: var(--theme-primary-color);
  width: 14px;
  height: 30px;
  top: 0;
  right: 0;
  margin-top: 1px;
  position: absolute;
}

.blink {
  animation: blinker 0.7s linear infinite;
}
@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>