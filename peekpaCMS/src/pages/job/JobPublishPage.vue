<script setup lang="ts">
import { AxiosError } from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { computed, reactive, ref } from 'vue';
import { type InternalRuleItem } from 'async-validator';
import { type JobCreate } from '../../types/Job';
import { createJob } from '../../services/job';

const loading = ref<boolean>(false);
const doubleCheck = ref<boolean>(false);
const ruleFormRef = ref<FormInstance>();

const experienceList = [
  '不需要经验',
  '经验0-2年',
  '经验2-5年',
  '经验5-10年',
  '经验10年以上',
];

const educationList = ['博士', '研究生', '大学', '高中', '初中', '初中以下'];

const form = reactive<JobCreate>({
  title: '',
  status: 0,
  city: '',
  location: '',
  salary_min: 0,
  salary_max: 0,
  salary_count: 12,
  hire_number: 1,
  experience: experienceList[0],
  benefit: '',
  description: '',
  education: '',
});

// 显示最终确认框
const goToDoublecheck = async () => {
  if (!ruleFormRef.value) return;
  await ruleFormRef.value.validate(async (valid: any) => {
    if (valid) {
      doubleCheck.value = true;
    } else {
      ElMessage.error('请检查表单内容');
      loading.value = false;
    }
  });
};

// 表单提交方法
const handleSubmit = async () => {
  loading.value = true;
  try {
    console.log('form: ', form);
    const response = await createJob(form);
    if (response.status === 201) {
      ElMessage.success('创建成功');
      // 重置表单
      ruleFormRef.value?.resetFields();
      doubleCheck.value = false;
    } else {
      ElMessage.error(`创建失败[${response.status}]`);
    }
    loading.value = false;
  } catch (error) {
    ElMessage.error(`创建失败[${(error as AxiosError).message}]`);
    loading.value = false;
  }
};

// 关闭确认框
const closeDialog = () => {
  doubleCheck.value = false;
};

// 重置表单数据
const resetForm = () => {
  if (ruleFormRef.value) {
    ruleFormRef.value.resetFields();
  }
};

// 格式化显示工资
const displaySalary = computed(() => {
  if (form.salary_max === form.salary_min) {
    return `${form.salary_min} 元     ${form.salary_count}薪`;
  }
  return `${form.salary_min} 元 ~ ${form.salary_max} 元     ${form.salary_count}薪`;
});
// 薪资自定义验证
const validateNumber = (
  _rule: InternalRuleItem,
  _value: number,
  callback: (error?: string | Error) => void
) => {
  if (
    form.salary_max > 0 &&
    form.salary_min > 0 &&
    Number(form.salary_max) >= Number(form.salary_min)
  ) {
    callback();
  } else {
    callback(new Error('请正确输入薪资数字'));
  }
};

// 表单验证
const rules = {
  title: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
  city: [{ required: true, message: '请输入工作所在城市', trigger: 'blur' }],
  location: [{ required: true, message: '请输入工作地址', trigger: 'blur' }],
  benefit: [{ required: true, message: '请输入职位福利', trigger: 'blur' }],
  education: [{ required: true, message: '请选择学历要求', trigger: 'blur' }],
  description: [
    { required: true, message: '请输入职位具体要求', trigger: 'blur' },
  ],
  salary: [{ validator: validateNumber, trigger: 'submit' }],
};

</script>

<template>
  <div class="container">
    <el-form
      ref="ruleFormRef"
      v-loading="loading"
      class="form-box"
      :rules="rules"
      :model="form"
      label-width="auto"
      label-position="top"
    >
      <el-form-item label="职位名称" prop="title">
        <el-input v-model="form.title"></el-input>
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="工作城市" prop="city">
            <el-input v-model="form.city"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="16">
          <el-form-item label="具体地址" prop="location">
            <el-input v-model="form.location"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="岗位薪资" prop="salary">
        <el-col :span="7">
          <el-input v-model="form.salary_min" type="number"
            ><template #append>元</template></el-input
          >
        </el-col>
        <el-col :span="1" class="text-center">
          <span class="text-gray-500">~</span>
        </el-col>
        <el-col :span="7">
          <el-input v-model="form.salary_max" type="number">
            <template #append>元</template></el-input
          >
        </el-col>
        <el-col :span="3" class="text-right">
          <span>一年</span>
        </el-col>
        <el-col :span="3">
          <el-input-number v-model="form.salary_count" :min="12" :max="50" />
        </el-col>
        <el-col :span="1" class="text-center">
          <span>薪</span>
        </el-col>
      </el-form-item>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="经验要求" prop="experience">
            <el-select v-model="form.experience">
              <el-option
                v-for="item in experienceList"
                :key="item"
                class=""
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="8">
          <el-form-item label="学历要求" prop="education">
            <el-select v-model="form.education" placeholder="请选择">
              <el-option
                v-for="item in educationList"
                :key="item"
                class=""
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="招聘人数" prop="hire">
            <el-input-number v-model="form.hire_number" :min="1" :max="100" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="职位福利" prop="benefit">
        <el-input
          v-model="form.benefit"
          :autosize="{ minRows: 2 }"
          type="textarea"
        ></el-input>
      </el-form-item>

      <el-form-item label="具体要求" prop="description">
        <el-input
          v-model="form.description"
          :autosize="{ minRows: 4 }"
          type="textarea"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="goToDoublecheck">创建</el-button>
        <el-button @click="resetForm">清空</el-button>
      </el-form-item>
    </el-form>

    <el-dialog v-model="doubleCheck" title="确定发布职位么" width="60%">
      <el-form
        v-loading="loading"
        :model="form"
        label-width="auto"
        label-position="right"
      >
        <el-form-item label="职位名称：">
          {{ form.title }}
        </el-form-item>

        <el-form-item label="工作城市：">
          {{ form.city }}
        </el-form-item>

        <el-form-item label="工作地点：">
          {{ form.location }}
        </el-form-item>

        <el-form-item label="岗位薪资：">
          {{ displaySalary }}
        </el-form-item>

        <el-form-item label="经验要求：">
          {{ form.experience }}
        </el-form-item>

        <el-form-item label="招聘人数：">
          {{ form.hire_number }} 人
        </el-form-item>

        <el-form-item label="职位福利：">
          {{ form.benefit }}
        </el-form-item>

        <el-form-item label="具体要求：">
          <pre>{{ form.description }}</pre>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="closeDialog">返回</el-button>
        </el-form-item>
      </el-form></el-dialog
    >
  </div>
</template>
<style scoped>
.text-center {
  text-align: center;
}
.text-right {
  text-align: end;
  margin-right: 1rem;
}
pre {
  white-space: pre-line;
}
</style>