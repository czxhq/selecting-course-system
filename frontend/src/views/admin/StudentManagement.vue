<template>
  <div class="teacher-management">
    <h2>学生管理</h2>

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
        >导入学生</el-button
      >
      <el-button type="primary" @click="triggerFileInput" size="small"
        >Excel批量导入学生信息</el-button
      >

      <input
        type="file"
        ref="fileInput"
        style="display: none"
        accept=".xlsx"
        @change="handleFileChange"
      />
    </div>

    <!-- 学生列表 -->
    <el-table :data="paginatedStudents" border style="width: 100%">
      <el-table-column label="学号" prop="Id" />
      <el-table-column label="姓名" prop="name" />
      <!-- 专业列 -->
      <el-table-column label="专业">
        <template #default="{ row }">
          <el-tag>{{ row.major }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button @click="resetPassword(row.Id)" size="small" type="primary"
            >重置密码</el-button
          >
          <el-button @click="deleteStudent(row.Id)" size="small" type="danger"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <el-pagination
      v-if="students.length > 0"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="students.length"
      layout="total, prev, pager, next, jumper"
      @current-change="handlePageChange"
    />

    <!-- 导入学生弹框 -->
    <el-dialog
      title="导入学生"
      :model-value="importDialogVisible"
      @update:model-value="importDialogVisible = $event"
      width="400px"
      @close="resetImportForm"
    >
      <el-form :model="importForm" ref="importFormRef">
        <el-form-item
          label="学号"
          prop="id"
          :rules="[{ required: true, message: '请输入学号', trigger: 'blur' }]"
        >
          <el-input v-model="importForm.id" />
        </el-form-item>
        <el-form-item
          label="姓名"
          prop="name"
          :rules="[
            { required: true, message: '请输入学生姓名', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.name" />
        </el-form-item>
        <!-- 新增专业选择框 -->
        <el-form-item
          label="专业"
          prop="major"
          :rules="[{ required: true, message: '请选择专业', trigger: 'blur' }]"
        >
          <el-radio-group v-model="importForm.major">
            <el-radio
              v-for="major in majors"
              :key="major.name"
              :label="major.name"
              >{{ major.name }}</el-radio
            >
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button @click="importTeacher" type="primary">提交</el-button>
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
const searchQuery = ref('')
const searchType = ref(undefined)
const students = ref([])
const originalStudents = ref([])
const paginatedStudents = ref([])
const currentPage = ref(1)
const pageSize = ref(20)

// 导入学生表单
const importDialogVisible = ref(false)
const importForm = ref({
  id: '',
  name: '',
  major: '' // 新增专业属性
})

// 存储专业数据
const majors = ref<any>([])

// 获取所有专业信息
const fetchMajors = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/getMajors/',
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    majors.value = response.data.majors || []
  } catch (error) {
    ElMessage.error('获取专业信息失败')
  }
}

// 获取所有学生信息
const fetchStudents = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/getAllStudent/',
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    students.value = response.data.data || []
    originalStudents.value = [...students.value]
    handlePageChange(1)
  } catch (error) {
    ElMessage.error('获取学生信息失败')
  }
}

// 处理分页变化
const handlePageChange = (page: any) => {
  currentPage.value = page
  const start = (page - 1) * pageSize.value
  const end = page * pageSize.value
  paginatedStudents.value = students.value.slice(start, end)
}

// 搜索学生
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
    type: 0,
    by: searchType.value
  }

  try {
    const response = await axiosrequest.post({
      url: '/admin/search/',
      data: queryData,
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    students.value = response.data.data || []
    handlePageChange(1)
  } catch (error) {
    ElMessage.error('搜索学生失败')
  }
}

// 清除搜索
const clearSearch = () => {
  searchQuery.value = ''
  students.value = [...originalStudents.value]
  handlePageChange(1)
}

// 搜索框输入变化时
const onSearchInputChange = () => {
  if (!searchQuery.value) {
    students.value = [...originalStudents.value]
    handlePageChange(1)
  }
}

// 导入学生
const openImportDialog = () => {
  importDialogVisible.value = true
}

// 提交导入学生
const importTeacher = async () => {
  if (importForm.value.id && importForm.value.name && importForm.value.major) {
    try {
      const response = await axiosrequest.post({
        url: '/admin/importStudent/',
        data: importForm.value,
        headers: {
          'Content-Type': 'application/json'
        } as AxiosRequestHeaders
      })
      if (response.data.result === 'success') {
        ElMessage.success('学生导入成功')
        fetchStudents()
        closeImportDialog()
      } else {
        ElMessage.error('学生导入失败')
      }
    } catch (error) {
      ElMessage.error('导入失败')
    }
  } else {
    ElMessage.warning('请填写完整的学生信息')
  }
}

// 关闭导入学生弹框
const closeImportDialog = () => {
  importDialogVisible.value = false
}

// 重置导入表单
const resetImportForm = () => {
  importForm.value.id = ''
  importForm.value.name = ''
  importForm.value.major = ''
}

// 重置密码
const resetPassword = async (id: string) => {
  ElMessageBox.confirm('确认重置密码？', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        const response = await axiosrequest.post({
          url: '/admin/reset/',
          data: { type: 0, id },
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

// 删除学生
const deleteStudent = async (id: string) => {
  ElMessageBox.confirm('确认删除该学生？', '警告', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        const response = await axiosrequest.post({
          url: '/admin/deleteStudent/',
          data: { id },
          headers: {
            'Content-Type': 'application/json'
          } as AxiosRequestHeaders
        })
        if (response.data.result === 'success') {
          ElMessage.success('学生删除成功')
          students.value = students.value.filter(
            (student: any) => student.Id !== id
          )
          handlePageChange(currentPage.value)
        } else {
          ElMessage.error('学生删除失败')
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
      url: 'admin/importBatchStudent/', // 导入教师接口
      data: formData,
      headers: {} as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('学生信息批量导入成功')
      fetchStudents()
    } else {
      ElMessage.error('学生信息批量导入失败')
    }
  } catch (error) {
    ElMessage.error('文件上传失败')
  }
}

// 页面加载时获取所有数据
onMounted(() => {
  fetchMajors() // 获取专业信息
  fetchStudents() // 获取学生数据
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
