<script setup lang="ts"></script>

<template>
  <div class="base_container container">
    <div class="center-xy">
      <p>404, 页面未找到...</p>
      <span class="handle blink"></span>
    </div>
  </div>
</template>

<style scoped>
.base_container {
  overflow: hidden;
  font-size: 16px;
  height: 100%;
  color: #000;
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
}
.handle {
  background: var(--theme-one-color);
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
.static_bottom {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
}
</style>