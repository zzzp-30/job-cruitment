<script setup lang="ts">
import { ref } from 'vue';

const time = ref<string>('');
const date = ref<string>('');

const week = [
  '星期天',
  '星期一',
  '星期二',
  '星期三',
  '星期四',
  '星期五',
  '星期六',
];

const zeroPadding = (num: number, digit: number) => {
  let zero = '';
  for (let i = 0; i < digit; i += 1) {
    zero += '0';
  }
  return (zero + num).slice(-digit);
};

// 更新时间
const updateTime = () => {
  const cd = new Date();
  time.value = `${zeroPadding(cd.getHours(), 2)}:${zeroPadding(
    cd.getMinutes(),
    2
  )}:${zeroPadding(cd.getSeconds(), 2)}`;
  date.value = `${zeroPadding(cd.getFullYear(), 4)}年${zeroPadding(
    cd.getMonth() + 1,
    2
  )}月${zeroPadding(cd.getDate(), 2)}日 ${week[cd.getDay()]}`;
};

setInterval(updateTime, 1000);
updateTime();
</script>

<template>
  <div id="clock">
    <p class="date">{{ date }}</p>
    <p class="time">{{ time }}</p>
  </div>
</template>

<style scoped>
p {
  margin: 0;
  padding: 0;
}
#clock {
  height: 100px;
  background: radial-gradient(
    ellipse at center,
    var(--theme-two-color) 0%,
    var(--theme-one-color) 70%
  );
  background-size: 100%;
  font-family: 'Share Tech Mono', monospace;
  text-align: center;
  color: var(--theme-three-color);
  text-shadow: 0 0 20px var(--theme-four-color), 0 0 20px var(--theme-one-color);
  border-radius: 4px;
}
.time {
  letter-spacing: 0.05em;
  font-size: 2.9rem;
  padding: 5px 0;
}
.date {
  padding-top: 10px;
  letter-spacing: 0.1em;
  font-size: 。6rem;
}
</style>