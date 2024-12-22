<template>
  <div class="notification-management">
    <h2>通知管理</h2>

    <div class="notification-list">
      <el-table :data="notifications" border style="width: 100%">
        <el-table-column label="通知标题" prop="title" />
        <el-table-column label="通知内容" prop="content" />
        <el-table-column label="发布日期" prop="date" />
      </el-table>

      <!-- 发布新通知按钮 -->
      <el-button
        @click="openDialog"
        type="primary"
        size="small"
        style="margin-top: 20px"
      >
        发布新通知
      </el-button>
    </div>

    <!-- 弹出表单框 -->
    <el-dialog
      title="发布新通知"
      :model-value="dialogVisible"
      @update:model-value="dialogVisible = $event"
      width="40%"
      @close="resetForm"
    >
      <el-form :model="form" ref="formRef" label-width="80px">
        <el-form-item label="通知标题" prop="title" :rules="titleRules">
          <el-input v-model="form.title" placeholder="请输入通知标题" />
        </el-form-item>

        <el-form-item label="通知内容" prop="content" :rules="contentRules">
          <el-input
            v-model="form.content"
            type="textarea"
            placeholder="请输入通知内容"
            :rows="4"
          />
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitNotification(formRef)"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import axiosrequest from '@/services'
import {
  ElMessage,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  type FormInstance
} from 'element-plus'
import type { AxiosRequestHeaders } from 'axios'

const notifications = ref<any[]>([]) // 存储通知列表
const dialogVisible = ref(false) // 控制弹窗的显示与隐藏
const form = ref({
  title: '',
  content: ''
}) // 表单数据
const formRef = ref<FormInstance>() // 表单引用

// 表单验证规则
const titleRules = [
  { required: true, message: '请输入通知标题', trigger: 'blur' }
]

const contentRules = [
  { required: true, message: '请输入通知内容', trigger: 'blur' }
]

// 获取通知列表
const fetchNotifications = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/getNotifications/', // 假设这是获取通知的API
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    notifications.value = response.data.data.messages
  } catch (error) {
    ElMessage.error('获取通知失败')
  }
}

// 弹出表单
const openDialog = () => {
  dialogVisible.value = true
  nextTick(() => {
    form.value.title = ''
    form.value.content = ''
  })
}

// 提交发布通知
const submitNotification = async (formRef: FormInstance | undefined) => {
  if (!formRef) {
    return
  }

  await formRef.validate((valid, fields) => {
    if (valid) {
      submitNotificationNet()
    }
  })
}

const submitNotificationNet = async () => {
  const notification = {
    title: form.value.title,
    content: form.value.content
  }

  try {
    // 发布通知请求
    const response = await axiosrequest.post({
      url: '/admin/notifications/', // 发布通知接口
      data: notification,
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })

    if (response.data.result === 'success') {
      ElMessage.success('通知发布成功')
      fetchNotifications() // 刷新通知列表
      dialogVisible.value = false // 关闭弹窗
    } else {
      ElMessage.error('通知发布失败')
    }
  } catch (error) {
    ElMessage.error('发布失败')
  }
}

// 重置表单
const resetForm = () => {
  form.value.title = ''
  form.value.content = ''
}

onMounted(() => {
  fetchNotifications() // 页面加载时获取通知列表
})
</script>

<style scoped>
/* 整体页面样式 */
.notification-management {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.notification-management h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

/* 通知列表样式 */
.notification-list {
  margin-top: 20px;
}

/* 表格样式 */
.el-table {
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.el-table th {
  background-color: #f4f4f4;
  color: #333;
  font-weight: bold;
  padding: 12px 10px;
}

.el-table .el-table-column {
  padding: 10px;
}

.el-table .el-button {
  padding: 6px 12px;
  border-radius: 4px;
}

.el-table .el-button[type='primary'] {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

.el-table .el-button[type='danger'] {
  background-color: #d9534f;
  border-color: #d9534f;
  color: white;
}

/* 发布新通知按钮样式 */
.el-button {
  padding: 8px 16px;
  border-radius: 4px;
}

.el-button[type='primary'] {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

.el-button[type='primary']:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

/* 弹窗样式调整 */
.el-dialog {
  border-radius: 8px;
}

.el-dialog .el-dialog__header {
  background-color: #409eff;
  color: white;
}

.el-dialog .el-dialog__body {
  padding: 20px;
  background-color: #f9f9f9;
}

.el-dialog .el-form-item {
  margin-bottom: 15px;
}

.el-dialog .el-button {
  padding: 10px 20px;
  border-radius: 4px;
}

.el-dialog .el-button[type='primary'] {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

.el-dialog .el-button[type='default'] {
  background-color: #f0f0f0;
  border-color: #e0e0e0;
  color: #333;
}

/* 弹窗底部按钮样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.dialog-footer .el-button {
  margin-left: 10px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .el-table {
    font-size: 12px;
  }

  .el-table .el-table-column {
    padding: 8px;
  }

  .el-button {
    width: 100%;
    margin-top: 10px;
  }
}
</style>
