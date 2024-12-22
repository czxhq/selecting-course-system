<template>
  <div class="teacher-management">
    <h2>教师管理</h2>

    <div class="search-area">
      <!-- 搜索类型选择框 -->
      <el-select
        v-model="searchType"
        placeholder="选择搜索类型"
        size="small"
        style="width: 200px"
      >
        <el-option label="按姓名搜索" value="0" />
        <el-option label="按编号搜索" value="1" />
      </el-select>

      <el-input
        v-model="searchQuery"
        placeholder="请输入搜索关键词"
        class="search-input"
        size="small"
        style="width: 300px; margin-right: 10px"
        @input="onSearchInputChange"
      />

      <el-button @click="searchTeachers" type="primary" size="small"
        >搜索</el-button
      >
      <el-button @click="clearSearch" type="warning" size="small"
        >清除搜索</el-button
      >
      <el-button @click="openImportDialog" type="success" size="small"
        >导入教师</el-button
      >
      <el-button type="primary" @click="triggerFileInput" size="small"
        >Excel批量导入教师信息</el-button
      >
      <input
        type="file"
        ref="fileInput"
        style="display: none"
        accept=".xlsx"
        @change="handleFileChange"
      />
    </div>

    <el-table :data="paginatedTeachers" border style="width: 100%">
      <el-table-column label="教师编号" prop="Id" />
      <el-table-column label="姓名" prop="name" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button @click="resetPassword(row.Id)" size="small" type="primary"
            >重置密码</el-button
          >
          <el-button @click="deleteTeacher(row.Id)" size="small" type="danger"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <el-pagination
      v-if="teachers.length > 0"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="teachers.length"
      layout="total, prev, pager, next, jumper"
      @current-change="handlePageChange"
    />

    <!-- 导入教师弹框 -->
    <el-dialog
      title="导入教师"
      :model-value="importDialogVisible"
      @update:model-value="importDialogVisible = $event"
      width="400px"
      @close="resetImportForm"
    >
      <el-form :model="importForm" ref="importFormRef">
        <el-form-item
          label="教师编号"
          prop="id"
          :rules="[
            { required: true, message: '请输入教师编号', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.id" />
        </el-form-item>
        <el-form-item
          label="姓名"
          prop="name"
          :rules="[
            { required: true, message: '请输入教师姓名', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.name" />
        </el-form-item>
        <el-form-item>
          <el-button @click="importTeacher(importFormRef)" type="primary"
            >提交</el-button
          >
          <el-button @click="closeImportDialog">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axiosrequest from '@/services'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import type { AxiosRequestHeaders } from 'axios'

// 搜索与分页
const searchQuery = ref('') // 搜索框的输入内容
const searchType = ref(undefined) // 默认为按姓名搜索
const teachers = ref([]) // 存储所有教师数据
const originalTeachers = ref([]) // 存储所有教师数据的副本，用于恢复
const paginatedTeachers = ref([]) // 当前分页的教师数据
const currentPage = ref(1) // 当前页
const pageSize = ref(20) // 每页显示条数

// 导入教师表单
const importDialogVisible = ref(false) // 控制导入教师弹框的显示
const importForm = ref({
  id: '',
  name: ''
}) // 导入表单的字段
const importFormRef = ref<FormInstance>()
// 获取所有教师信息
const fetchTeachers = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/getAllTeacher/', // 获取所有教师的接口路径
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    teachers.value = response.data.data || [] // 保存获取到的教师数据
    originalTeachers.value = [...teachers.value] // 保存原始教师列表，用于恢复
    handlePageChange(1) // 加载数据后初始化分页
  } catch (error) {
    ElMessage.error('获取教师信息失败')
  }
}

// 处理分页变化
const handlePageChange = (page: any) => {
  currentPage.value = page
  const start = (page - 1) * pageSize.value
  const end = page * pageSize.value
  paginatedTeachers.value = teachers.value.slice(start, end)
}

// 搜索教师
const searchTeachers = async () => {
  if (!searchQuery.value) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  if (!searchType.value) {
    ElMessage.warning('请选择搜索类型')
    return
  }

  const queryData = {
    query: searchQuery.value,
    type: 1, // 默认为教师搜索
    by: searchType.value // 按选择的方式搜索
  }

  try {
    const response = await axiosrequest.post({
      url: '/admin/search/', // 搜索接口路径
      data: queryData,
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    teachers.value = response.data.data || [] // 更新教师列表
    handlePageChange(1) // 更新分页
  } catch (error) {
    ElMessage.error('搜索教师失败')
  }
}

// 清除搜索
const clearSearch = () => {
  searchQuery.value = '' // 清空搜索框
  teachers.value = [...originalTeachers.value] // 恢复显示所有教师数据
  handlePageChange(1) // 恢复分页
}

// 搜索框输入变化时
const onSearchInputChange = () => {
  if (!searchQuery.value) {
    teachers.value = [...originalTeachers.value] // 搜索框为空时恢复原始数据
    handlePageChange(1) // 恢复分页
  }
}

// 导入教师
const openImportDialog = () => {
  importDialogVisible.value = true // 显示导入教师表单
}

// 提交导入教师
const importTeacher = async (formRef: FormInstance | undefined) => {
  if (!formRef) {
    return
  }

  await formRef.validate((valid, fields) => {
    if (valid) {
      submitImportTeacherNet()
    }
  })
}

const submitImportTeacherNet = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/importTeacher/', // 导入教师接口
      data: importForm.value,
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('教师导入成功')
      fetchTeachers() // 导入成功后刷新教师列表
      closeImportDialog() // 关闭弹框
    } else {
      ElMessage.error('教师导入失败')
    }
  } catch (error) {
    ElMessage.error('导入失败')
  }
}

// 关闭导入教师弹框
const closeImportDialog = () => {
  importDialogVisible.value = false
}

// 重置导入表单
const resetImportForm = () => {
  importForm.value.id = ''
  importForm.value.name = ''
}

// 重置密码
const resetPassword = async (id: string) => {
  ElMessageBox.confirm('确认重置密码？', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning' // 正确的合法值应为 "warning"
  })
    .then(async () => {
      try {
        const response = await axiosrequest.post({
          url: '/admin/reset/', // 重置密码接口
          data: { type: 1, id },
          headers: {
            'Content-Type': 'application/json'
          } as AxiosRequestHeaders
        })
        if (response.data.result === 'success') {
          ElMessage.success('密码重置成功')
        } else {
          ElMessage.error('密码重置失败')
        }
      } catch (error) {
        ElMessage.error('重置密码失败')
      }
    })
    .catch(() => {
      ElMessage.info('操作已取消')
    })
}

// 删除教师
const deleteTeacher = async (id: string) => {
  ElMessageBox.confirm('确认删除该教师？', '警告', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        const response = await axiosrequest.post({
          url: '/admin/deleteTeacher/', // 删除教师接口
          data: { id },
          headers: {
            'Content-Type': 'application/json'
          } as AxiosRequestHeaders
        })
        if (response.data.result === 'success') {
          ElMessage.success('教师删除成功')
          // 删除成功后从教师列表中移除该教师
          teachers.value = teachers.value.filter(
            (teacher: any) => teacher.Id !== id
          )
          handlePageChange(currentPage.value) // 更新分页
        } else {
          ElMessage.error('教师删除失败')
        }
      } catch (error) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      ElMessage.info('操作已取消')
    })
}

const fileInput = ref<HTMLInputElement | null>(null)

const triggerFileInput = () => {
  // 通过代码触发文件选择框
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// 文件选择后的处理
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files ? input.files[0] : null

  if (file) {
    // 创建FormData并上传文件
    const formData = new FormData()
    formData.append('file', file)

    // 上传文件的请求
    uploadFile(formData)
  }
}

// 上传文件
const uploadFile = async (formData: FormData) => {
  // 使用axios上传文件

  try {
    const response = await axiosrequest.post({
      url: 'admin/importBatchTeacher/', // 导入教师接口
      data: formData,
      headers: {} as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('教师信息批量导入成功')
      fetchTeachers()
    } else {
      ElMessage.error('教师信息批量导入失败')
    }
  } catch (error) {
    ElMessage.error('文件上传失败')
  }
}

// 页面加载时获取所有教师信息
onMounted(() => {
  fetchTeachers()
})
</script>

<style scoped>
/* 整体页面样式 */
.teacher-management {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.teacher-management h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

/* 搜索区样式 */
.search-area {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.search-area .el-select,
.search-area .el-input,
.search-area .el-button {
  font-size: 14px;
  border-radius: 4px;
}

.search-area .el-select {
  width: 220px;
}

.search-area .el-input {
  width: 300px;
}

.search-area .el-button {
  padding: 8px 16px;
}

.search-area .el-button[type='primary'] {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

.search-area .el-button[type='warning'] {
  background-color: #f0ad4e;
  border-color: #f0ad4e;
  color: white;
}

.search-area .el-button[type='success'] {
  background-color: #5cb85c;
  border-color: #5cb85c;
  color: white;
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

.el-table .el-table-column .el-tag {
  background-color: #d1e8e2;
  color: #00796b;
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

/* 分页器样式 */
.el-pagination {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #eaeaea;
  text-align: center;
}

.el-pagination .el-pagination__total {
  color: #666;
}

/* 导入学生弹框样式 */
.el-dialog {
  border-radius: 8px;
}

.el-dialog .el-dialog__header {
  background-color: #5cb85c;
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

/* 响应式布局 */
@media (max-width: 768px) {
  .search-area {
    flex-direction: column;
    align-items: stretch;
  }

  .search-area .el-select,
  .search-area .el-input,
  .search-area .el-button {
    width: 100%;
    margin-bottom: 10px;
  }

  .el-table {
    width: 100%;
    font-size: 12px;
  }

  .el-table .el-table-column {
    padding: 8px;
  }
}
</style>
