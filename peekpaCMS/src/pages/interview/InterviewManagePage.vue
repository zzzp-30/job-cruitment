<script setup lang="ts">
import {
  ElMessage,
  ElMessageBox,
  type FormInstance,
  type InputInstance,
} from 'element-plus';
import { nextTick, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { UNAUTH_401 } from '../../services/Axios';
import {
  getAllInterviews,
  searchInterview,
  getAllJobName,
  createInvitation,
  updateInterview,
} from '../../services/interview';
import { timeStampFormat } from '../../utils/helper';
import type {
  JobNameItem,
  ResponseInterviewList,
  Interview,
  InterviewInvitation,
} from '../../types/Interview';
import { AxiosError } from 'axios';

const route = useRoute();

interface MessageForm {
  jobId: string;
  id: string;
  candidateId: string;
  message: string;
  name: string;
  status: number;
}

interface UpdateInterviewForm {
  index: number;
  id: string;
  iid: string;
  feedback: JSON;
  status: number;
  nextRound: string;
  nextFeedback: string;
}

const updateForm = reactive<UpdateInterviewForm>({
  index: -1,
  id: '',
  iid: '',
  feedback: {} as JSON,
  status: -1,
  nextRound: '',
  nextFeedback: '',
});

const messageForm = reactive<MessageForm>({
  jobId: '',
  id: '',
  candidateId: '',
  message: '',
  name: '',
  status: 0,
});

const LIMIT = 10;
let curOffset = 0;

const interviewStatus = [
  '第1轮',
  '第2轮',
  '第3轮',
  'HR轮',
  '通过',
  '不合格',
  '已拒绝',
];

const currentJob = ref<string>('all');
const nameList = ref<JobNameItem[]>([]);
const data = ref<ResponseInterviewList>();
const curPage = ref<number>(1);
const total = ref<number>(0);
const updateFormRef = ref<FormInstance>();
const showUpdate = ref<boolean>(false);
const dialogInput = ref<InputInstance>();
const loading = ref<boolean>(false);
const search = ref<string>('');
const showMessage = ref<boolean>(false);

// 请求职位名称
const requestJobNameData = async () => {
  try {
    const response = await getAllJobName();
    if (response.status === 200) {
      nameList.value = response.data;
      nameList.value.splice(0, 0, {
        id: 'all',
        title: '全部',
      });
    }
  } catch (error) {
    if ((error as Error).message !== UNAUTH_401) {
      ElMessage.error(`网络请求错误[${error}]`);
    }
  }
};

// 显示这一轮面试进度
const displayNextRound = () => {
  return `本次反馈(${updateForm.nextRound})`;
};

// 创建面试邀请消息
const sendInvitation = async () => {
  try {
    const response = await createInvitation(
      messageForm.jobId,
      messageForm.id,
      messageForm.candidateId,
      messageForm.message,
      messageForm.status
    );
    if (response.status === 201) {
      ElMessage.success('已发送邀请信息');
      messageForm.jobId = '';
      messageForm.id = '';
      messageForm.candidateId = '';
      messageForm.message = '';
      messageForm.name = '';
      await requestData(currentJob.value, curOffset);
    }
    showMessage.value = false;
  } catch (error) {
    showMessage.value = false;
    ElMessage.error(`发送邀请失败`);
  }
};

// 更新面试情况
const handleUpdate = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid: boolean) => {
    if (valid) {
      try {
        updateForm.feedback = {
          ...updateForm.feedback,
          [updateForm.nextRound]: updateForm.nextFeedback,
        };
        const response = await updateInterview(updateForm.id, updateForm.iid, {
          status: updateForm.status,
          feedback: updateForm.feedback,
        });
        if (response.status === 200) {
          ElMessage.success('更新成功');
          showUpdate.value = false;
          if (data.value !== undefined) {
            data.value.results[updateForm.index] = response.data;
          }
          updateForm.index = -1;
          formEl.resetFields();
        } else {
          ElMessage.error(`更新失败[${response.status}]`);
        }
      } catch (error) {
        ElMessage.error(`更新失败`);
      }
    } else {
      ElMessage.error('请仔细检查表单');
    }
  });
};

// 请求数据
const requestData = async (id: string, offset: number) => {
  loading.value = true;
  try {
    const response = await getAllInterviews(id, LIMIT, offset);
    if (response.status === 200) {
      data.value = response.data;
      total.value = response.data.count;
      curPage.value = curOffset / LIMIT + 1;
    }
    loading.value = false;
  } catch (error) {
    if ((error as Error).message !== UNAUTH_401) {
      ElMessage.error(`网络请求错误[${error}]`);
    }
    loading.value = false;
  }
};

// 搜索面试
const searchData = async (q: string, offset: number) => {
  loading.value = true;
  try {
    const response = await searchInterview(currentJob.value, q, LIMIT, offset);
    if (response.status === 200) {
      data.value = response.data;
      total.value = response.data.count;
      curPage.value = curOffset / LIMIT + 1;
    }
    loading.value = false;
  } catch (error) {
    if ((error as Error).message !== UNAUTH_401) {
      ElMessage.error(`网络请求错误[${error}]`);
    }
    loading.value = false;
  }
};

// 第一次进入页面，判断请求是否携带职位 ID，如果携带，则直接按照职位 ID 搜索，否则就返回全部面试信息
onMounted(async () => {
  await requestJobNameData();
  if (route.query.jobId) {
    currentJob.value = route.query.jobId as string;
  }
  await requestData(currentJob.value, 0);
});

// 页面跳转
const handlePageChange = async (value: number) => {
  curOffset = (value - 1) * LIMIT;
  await requestData(currentJob.value, curOffset);
};

// 显示填写反馈对话框
const showUpdateWindow = (index: number, item: Interview) => {
  console.log('index: ', index, 'item:', item);
};

// 拒绝操作
const handleDelete = (index: number, item: Interview) => {
  ElMessageBox.confirm(
    `确定要拒绝求职者 ${item.candidate.name} 的申请么?`,
    '警告',
    {
      confirmButtonText: '拒绝',
      cancelButtonText: '取消',
      type: 'error',
    }
  )
    .then(async () => {
      const response = await updateInterview(item.job.id, item.id, {
        status: 5,
      });
      if (response.status === 200) {
        ElMessage.success('更新成功');
        if (data.value !== undefined) {
          data.value.results[index] = response.data;
        }
      } else {
        ElMessage.error(`更新失败[${response.status}]`);
      }
    })
    .catch((error: any) => {
      if (
        (error as AxiosError).name !== 'CanceledError' &&
        error !== 'cancel'
      ) {
        ElMessage.error('更新网络错误');
      }
    });
};

const handleDialogOpen = () => {
  nextTick(() => {
    if (dialogInput.value) {
      dialogInput.value.focus();
    }
  });
};

// 出发搜索
const handleSearch = async () => {
  curOffset = 0;
  await searchData(search.value, curOffset);
};

// 清空搜索框
const clearSearch = async () => {
  curOffset = 0;
  await requestData(currentJob.value, curOffset);
};

// 出发列表内容转化
const changeSelectJob = async (id: string) => {
  await requestData(id, 0);
};

// 判断状态
const pendingInvitation = (invitation: InterviewInvitation | null) => {
  if (!invitation) return true;
  if (invitation.response === 0) {
    return true;
  }
  return false;
};

// 进度列内容
const displayStatus = (interview: Interview) => {
  let message = interviewStatus[interview.status];
  if (interview.status < 4 && pendingInvitation(interview.invitation)) {
    message = `${message}前`;
  }
  return message;
};

// 动态生产进度列样式
const displayStatusClass = (interview: Interview) => {
  if (interview.status === 4) {
    return 'success';
  }
  if (interview.status === 5 || interview.status === 6) {
    return 'danger';
  }
  return 'default';
};

// 展示最新面试反馈
const displayFeedback = (feedback: JSON) => {
  if (Object.keys(feedback).length === 0) {
    return '无';
  }
  return `${
    Object.keys(feedback)[Object.keys(feedback).length - 1]
  }：${Object.values(feedback).pop()}`;
};

// 判断面试邀请是否过期
const invitationIsExpired = (time: string) => {
  return new Date(time) < new Date();
};

// 动态生产 HTML 内容
const invitationHTML = (message: string, time: string, update?: string) => {
  const timeString = timeStampFormat(time);
  let result = `<p>信息：${message}</p><p>发送于： ${timeString}</p>`;
  if (update) {
    const updateTime = timeStampFormat(update);
    result = `${result}<p>更新于： ${updateTime}</p>`;
  }
  return result;
};

// 显示面试邀请发送窗口
const showMessageWindow = (item: Interview) => {
  showMessage.value = true;
  messageForm.jobId = item.job.id;
  messageForm.id = item.id;
  messageForm.candidateId = item.candidate.uid;
  messageForm.name = item.candidate.name;
  messageForm.status = item.status;
};
// 格式化显示时间
const displayTime = (time: string) => {
  return timeStampFormat(time);
};

// 禁止按键
const isDisabled = (item: Interview) => {
  if (
    item.invitation?.response === 2 ||
    item.status === 4 ||
    item.status === 5 ||
    item.status === 6
  ) {
    return true;
  }
  return false;
};

// 职位 URL
const getJobURL = (item: Interview) => {
  return `http://localhost:001/api/#/job/${item.id}/`;
};

// 简历下载 URL
const getResumeURL = (path: string) => {
  return `http://localhost:8001/${path}/`;
};

// 判断面试状态
const isPending = (item: Interview) => {
  return !item.invitation || item.invitation.response === 0;
};

// 判断按钮颜色
const getButtonType = (item: Interview) => {
  return isPending(item) && [1, 2, 3, 0].indexOf(item.status) !== -1
    ? 'warning'
    : 'primary';
};

// 获取面试者姓名
const getCandidateName = () => {
  return `发送邀请给 ${messageForm.name}`;
};
</script>

<template>
  <div class="container">
    <el-row class="search_main">
      <el-col :span="6">
        <el-select
          v-model="currentJob"
          default-first-option
          placeholder="工作名称"
          @change="changeSelectJob($event)"
        >
          <el-option
            v-for="item in nameList"
            :key="item.id"
            class=""
            :label="item.title"
            :value="item.id"
          >
            <span style="float: left">{{ item.title }}</span>
            <span
              style="
                float: right;
                color: var(--el-text-color-secondary);
                font-size: 13px;
              "
              >#{{ item.id }}</span
            ></el-option
          >
        </el-select>
      </el-col>
      <el-col :span="6" :offset="12">
        <el-input
          v-model="search"
          prefix-icon="eli-Search"
          placeholder="搜索"
          clearable
          @keyup.enter="handleSearch"
          @clear="clearSearch"
      /></el-col>
    </el-row>

    <el-table
      v-loading="loading"
      border
      header-cell-class-name="table-header"
      :data="data?.results"
    >
      <el-table-column label="职位名称">
        <template #default="scope">
          <el-link type="primary" :href="getJobURL(scope.row)">
            {{ scope.row.job.title }}</el-link
          >
        </template>
      </el-table-column>

      <el-table-column label="求职者" width="130">
        <template #default="scope">
          {{ scope.row.candidate.name }}
        </template>
      </el-table-column>
      <el-table-column label="简历" width="150">
        <template #default="scope">
          <el-link type="primary" :href="getResumeURL(scope.row.resume.url)"
            ><el-icon><eli-Download /></el-icon
            >{{ scope.row.resume.name }}</el-link
          >
        </template>
      </el-table-column>

      <el-table-column label="进度" width="90">
        <template #default="scope">
          <el-text :type="displayStatusClass(scope.row)">
            {{ displayStatus(scope.row) }}
          </el-text>
        </template>
      </el-table-column>

      <el-table-column label="状态" width="125">
        <template #default="scope">
          <el-text
            v-if="
              scope.row.status == 4 ||
              scope.row.status == 5 ||
              scope.row.status == 6
            "
          >
            已结束
          </el-text>
          <el-button
            v-else-if="scope.row.invitation === null"
            type="primary"
            text
            bg
            :disabled="isDisabled(scope.row)"
            @click="showMessageWindow(scope.row)"
            >未发送邀请</el-button
          >
          <el-button
            v-else-if="
              scope.row.invitation.response === 0 &&
              invitationIsExpired(scope.row.invitation.due_time)
            "
            type="primary"
            text
            bg
            :disabled="isDisabled(scope.row)"
            @click="showMessageWindow(scope.row)"
            >已经过期</el-button
          >
          <el-tooltip
            v-else-if="
              scope.row.invitation.response === 0 &&
              !invitationIsExpired(scope.row.invitation.due_time)
            "
            :content="
              invitationHTML(
                scope.row.invitation.message,
                scope.row.invitation.publish_time
              )
            "
            raw-content
          >
            <el-text type="warning">未回复</el-text>
          </el-tooltip>
          <el-tooltip
            v-else-if="
              scope.row.invitation.response === 1 &&
              !invitationIsExpired(scope.row.invitation.due_time)
            "
            :content="
              invitationHTML(
                scope.row.invitation.message,
                scope.row.invitation.publish_time,
                scope.row.invitation.update_time
              )
            "
            raw-content
          >
            <el-text class="mx-1" type="success" tag="b">已同意</el-text>
          </el-tooltip>
          <el-tooltip
            v-else-if="scope.row.invitation.response === 2"
            :content="
              invitationHTML(
                scope.row.invitation.message,
                scope.row.invitation.publish_time,
                scope.row.invitation.update_time
              )
            "
            raw-content
          >
            <el-text class="mx-1" type="danger" tag="b">已拒绝</el-text>
          </el-tooltip>
          <el-tooltip
            v-else-if="scope.row.invitation.response === 3"
            :content="
              invitationHTML(
                scope.row.invitation.message,
                scope.row.invitation.publish_time,
                scope.row.invitation.update_time
              )
            "
            raw-content
          >
            <el-text class="mx-1" type="danger" tag="b">已取消</el-text>
          </el-tooltip>
        </template>
      </el-table-column>

      <el-table-column label="最新面试反馈" width="200">
        <template #default="scope">
          {{ displayFeedback(scope.row.feedback) }}
        </template>
      </el-table-column>

      <el-table-column label="创建时间" width="170">
        <template #default="scope">
          {{ displayTime(scope.row.publish_time) }}
        </template>
      </el-table-column>

      <el-table-column width="200">
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <div>操作</div>
          </div>
        </template>
        <template #default="scope">
          <el-button
            size="small"
            icon="eli-document"
            :type="getButtonType(scope.row)"
            plain
            :disabled="isDisabled(scope.row) || isPending(scope.row)"
            @click="showUpdateWindow(scope.$index, scope.row)"
            >填写反馈</el-button
          >
          <el-button
            size="small"
            type="danger"
            icon="eli-close"
            plain
            :disabled="isDisabled(scope.row)"
            @click="handleDelete(scope.$index, scope.row)"
            >拒绝</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination_main"
      background
      layout="prev, pager, next"
      :current-page="curPage"
      :total="total"
      :page-size="LIMIT"
      @current-change="handlePageChange"
    ></el-pagination>
    <el-dialog
      v-model="showUpdate"
      title="填写面试反馈信息"
      width="50%"
      @open="handleDialogOpen"
    >
      <el-form ref="updateFormRef" :model="updateForm">
        <div
          v-if="updateForm.feedback && Object.keys(updateForm.feedback).length"
        >
          <el-form-item label="历史记录">
            <el-col
              v-for="(value, key) in updateForm.feedback"
              :key="key"
              :offset="2"
              :span="22"
            >
              <el-row>
                <el-col :span="4">{{ key }}</el-col>
                <el-col :span="20">{{ value }}</el-col>
              </el-row>
            </el-col>
          </el-form-item>
        </div>
        <el-form-item :label="displayNextRound()" prop="description">
          <el-input
            v-model="updateForm.nextFeedback"
            :autosize="{ minRows: 4 }"
            type="textarea"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showUpdate = false">取消</el-button>
          <el-button type="primary" @click="handleUpdate(updateFormRef)"
            >提交</el-button
          >
        </span>
      </template>
    </el-dialog>
    <el-dialog v-model="showMessage" :title="getCandidateName()" width="50%">
      <el-form :model="messageForm">
        <el-form-item label="消息内容" prop="description">
          <el-input
            v-model="messageForm.message"
            :autosize="{ minRows: 4 }"
            type="textarea"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showMessage = false">取消</el-button>
          <el-button type="primary" @click="sendInvitation()"
            >发送邀请</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.pagination_main {
  margin-top: 20px;
}

.search_main {
  margin-bottom: 20px;
}
</style>
