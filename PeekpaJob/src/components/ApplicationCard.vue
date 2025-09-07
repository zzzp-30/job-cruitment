<script setup lang="ts">
import { computed } from 'vue';
import type { UserApplication } from '../types/User';

// 定义组件props
const props = defineProps<{
  item: UserApplication; // 职位卡片数据
}>();

const statusList = [
  '第一轮面试',
  '第二轮面试',
  '第三轮面试',
  'HR轮面试',
  '通过',
  '不合格',
  '已拒绝',
];

// 计算属性，显示公司labels
const displaySalary = computed(() => {
  const max = Number((props.item.salary_max / 1000).toFixed(1));
  const min = Number((props.item.salary_min / 1000).toFixed(1));
  if (max === min) {
    return `${max}K`;
  }
  return `${min}K~${max}K`;
});

// 格式化显示时间
const displayTime = computed(() => {
  const date: Date = new Date(props.item.timestamp);
  const year: number = date.getFullYear();
  const month: string = String(date.getMonth() + 1).padStart(2, '0');
  const day: string = String(date.getDate()).padStart(2, '0');
  const hours: string = String(date.getHours()).padStart(2, '0');
  const minutes: string = String(date.getMinutes()).padStart(2, '0');
  return `${year}年${month}月${day}日 ${hours}点${minutes}分`;
});

// 职位 URL
const getJobUrl = computed(() => {
  return `http://localhost:8081/#/job/${props.item.id}/`;
});

const emit = defineEmits<{
  // 将搜索的点击事件交由父组件处理
  (eventName: 'updateResponse', id: string, value: number): void;
}>();

// 更新面试邀请消息
const replyInvitation = (value: number) => {
  emit('updateResponse', props.item.invitation.id, value);
};

// 显示面试进度
const displayStatus = computed(() => {
  if (props.item) {
    return statusList[props.item.status];
  }
  return null;
});

// 动态处理面试申请进度的 class 属性
const statusClass = computed(() => {
  if (props.item) {
    switch (props.item.status) {
      case 0:
      case 1:
      case 2:
      case 3:
        return 'processing';
      case 5:
      case 6:
        return 'failed';
      default:
        return 'pass';
    }
  }
  return 'processing';
});
</script>

<template>
  <el-card shadow="hover" :body-style="{ padding: '0px' }" class="card">
    <el-row class="first_row">
      <el-col :span="10" class="vertical_center">
        <div>
          <el-link class="title" :href="getJobUrl" target="_blank">{{
            item.title
          }}</el-link>
        </div>
      </el-col>
      <el-col :span="8" class="vertical_center">
        <div>
          {{ item.company_name }} /
          <span class="salary">{{ displaySalary }}</span>
        </div>
      </el-col>
      <el-col :span="6" class="time"> 申请时间：{{ displayTime }}</el-col>
      <div :class="`${statusClass} status`">{{ displayStatus }}</div>
    </el-row>
    <el-row v-if="item.invitation" class="second_row invitation">
      <el-col :span="20">{{ item.invitation.message }}</el-col>
      <el-col v-if="item.invitation.response === 0" :span="4">
        <el-button type="success" @click="replyInvitation(1)">同意</el-button>
        <el-button type="danger" @click="replyInvitation(2)">拒绝</el-button>
      </el-col>
      <el-col v-else-if="item.invitation.response === 1" :span="4">
        <el-button type="success" disabled>已同意</el-button>
        <el-button plain disabled>拒绝</el-button>
      </el-col>
      <el-col v-else-if="item.invitation.response === 2" :span="4">
        <el-button plain disabled>同意</el-button>
        <el-button type="danger" disabled>已拒绝</el-button>
      </el-col>
    </el-row>
  </el-card>
</template>

<style scoped>
.card {
  margin-top: 20px;
}
.first_row {
  padding: 15px 20px 15px 20px;
}
.second_row {
  padding: 15px 20px 15px 20px;
  background-color: rgb(250, 250, 250);
}

.status {
  position: absolute;
  top: 0;
  font-size: 0.8rem;
  font-weight: bold;
  right: 0;
  padding: 5px 20px;
  border-bottom-left-radius: 3px;
}

.processing {
  background-color: #409eff;
  color: #ffffff;
}

.pass {
  background-color: #67c23a;
  color: #ffffff;
}

.failed {
  background-color: #f56c6c;
  color: #ffffff;
}

.time {
  color: #545454;
  font-size: 0.8rem;
  text-align: right;
  margin-top: 20px;
}
.title {
  color: var(--theme-primary-color);
  font-size: 1.3rem;
  font-weight: bold;
}

.vertical_center {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.salary {
  color: #e31117;
  font-weight: 700;
}
</style>