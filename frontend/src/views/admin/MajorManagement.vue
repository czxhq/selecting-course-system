<template>
  <div class="teacher-management">
    <h2>专业管理</h2>

    <div class="search-area">
      <el-button @click="openImportDialog" type="success" size="small"
        >导入专业</el-button
      >
    </div>

    <el-table :data="majors" border style="width: 100%">
      <el-table-column label="专业名称" prop="name" />
      <el-table-column label="必修课总学分" prop="csum" />
      <el-table-column label="选修课总学分" prop="esum" />
      <el-table-column label="一般专业总学分" prop="gmsum" />
      <el-table-column label="核心专业总学分" prop="cmsum" />
      <el-table-column label="核心通识总学分" prop="cgsum" />
      <el-table-column label="一般通识总学分" prop="gsum" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button @click="openEditDialog(row)" size="small" type="primary"
            >修改</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 导入专业弹框 -->
    <el-dialog
      title="导入专业"
      :model-value="importDialogVisible"
      @update:model-value="importDialogVisible = $event"
      width="400px"
    >
      <el-form :model="importForm" ref="importFormRef">
        <el-form-item
          label="专业名称"
          prop="name"
          :rules="[
            { required: true, message: '请输入专业名称', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.name" />
        </el-form-item>
        <el-form-item
          label="必修课总学分"
          prop="csum"
          :rules="[
            { required: true, message: '请输入必修课总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.csum" />
        </el-form-item>
        <el-form-item
          label="选修课总学分"
          prop="esum"
          :rules="[
            { required: true, message: '请输入选修课总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.esum" />
        </el-form-item>
        <el-form-item
          label="一般专业总学分"
          prop="gmsum"
          :rules="[
            { required: true, message: '请输入一般专业总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.gmsum" />
        </el-form-item>
        <el-form-item
          label="核心专业总学分"
          prop="cmsum"
          :rules="[
            { required: true, message: '请输入核心专业总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.cmsum" />
        </el-form-item>
        <el-form-item
          label="核心通识总学分"
          prop="cgsum"
          :rules="[
            { required: true, message: '请输入核心通识总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.cgsum" />
        </el-form-item>
        <el-form-item
          label="一般通识总学分"
          prop="gsum"
          :rules="[
            { required: true, message: '请输入一般通识总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="importForm.gsum" />
        </el-form-item>
        <el-form-item>
          <el-button @click="importMajor(importFormRef)" type="primary"
            >提交</el-button
          >
          <el-button @click="closeImportDialog">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 修改专业弹框 -->
    <el-dialog
      title="修改专业"
      :model-value="editDialogVisible"
      width="400px"
      @update:model-value="editDialogVisible = $event"
    >
      <el-form :model="editForm" ref="editFormRef">
        <el-form-item
          label="必修课总学分"
          prop="csum"
          :rules="[
            { required: true, message: '请输入必修课总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="editForm.csum" />
        </el-form-item>
        <el-form-item
          label="选修课总学分"
          prop="esum"
          :rules="[
            { required: true, message: '请输入选修课总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="editForm.esum" />
        </el-form-item>
        <el-form-item
          label="一般专业总学分"
          prop="gmsum"
          :rules="[
            { required: true, message: '请输入一般专业总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="editForm.gmsum" />
        </el-form-item>
        <el-form-item
          label="核心专业总学分"
          prop="cmsum"
          :rules="[
            { required: true, message: '请输入核心专业总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="editForm.cmsum" />
        </el-form-item>
        <el-form-item
          label="核心通识总学分"
          prop="cgsum"
          :rules="[
            { required: true, message: '请输入核心通识总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="editForm.cgsum" />
        </el-form-item>
        <el-form-item
          label="一般通识总学分"
          prop="gsum"
          :rules="[
            { required: true, message: '请输入一般通识总学分', trigger: 'blur' }
          ]"
        >
          <el-input v-model="editForm.gsum" />
        </el-form-item>
        <el-form-item>
          <el-button @click="alterMajor(editFormRef)" type="primary"
            >提交</el-button
          >
          <el-button @click="closeEditDialog">取消</el-button>
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
const majors = ref<any[]>([])

const importDialogVisible = ref(false) // 控制导入教师弹框的显示
const importFormRef = ref<FormInstance>()
const importForm = ref({
  name: '',
  csum: '',
  esum: '',
  gmsum: '',
  cmsum: '',
  cgsum: '',
  gsum: ''
})

const editDialogVisible = ref(false) // 控制导入教师弹框的显示
const editFormRef = ref<FormInstance>()
const editForm = ref({
  name: '',
  csum: '',
  esum: '',
  gmsum: '',
  cmsum: '',
  cgsum: '',
  gsum: ''
})

const openEditDialog = (row: any) => {
  editForm.value = {
    name: row.name,
    csum: row.csum,
    esum: row.esum,
    gmsum: row.gmsum,
    cmsum: row.cmsum,
    cgsum: row.cgsum,
    gsum: row.gsum
  }
  editDialogVisible.value = true
}

const closeEditDialog = () => {
  editDialogVisible.value = false
  resetEditForm()
}

const resetEditForm = () => {
  editForm.value.name = ''
  editForm.value.csum = ''
  editForm.value.esum = ''
  editForm.value.gmsum = ''
  editForm.value.cmsum = ''
  editForm.value.cgsum = ''
  editForm.value.gsum = ''
}

const openImportDialog = () => {
  importDialogVisible.value = true
}

const closeImportDialog = async () => {
  importDialogVisible.value = false
  resetImportForm()
}

const resetImportForm = () => {
  importForm.value.name = ''
  importForm.value.csum = ''
  importForm.value.esum = ''
  importForm.value.gmsum = ''
  importForm.value.cmsum = ''
  importForm.value.cgsum = ''
  importForm.value.gsum = ''
}

const importMajor = async (importFormRef: FormInstance | undefined) => {
  if (!importFormRef) {
    return
  }
  await importFormRef.validate((valid, fields) => {
    if (valid) {
      submitMajorNet()
    }
  })
}

const alterMajor = async (alterFormRef: FormInstance | undefined) => {
  if (!alterFormRef) {
    return
  }
  await alterFormRef.validate((valid, fields) => {
    if (valid) {
      alterMajorNet()
    }
  })
}

const submitMajorNet = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/addMajor/', // 导入教师接口
      data: importForm.value,
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('专业导入成功')
      fetchMajors() // 导入成功后刷新教师列表
      closeImportDialog() // 关闭弹框
    } else {
      ElMessage.error('专业导入失败')
    }
  } catch (error) {
    ElMessage.error('网络问题，导入失败')
  }
}

const alterMajorNet = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/alterMajor/', // 导入教师接口
      data: editForm.value,
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('专业修改成功')
      fetchMajors() // 导入成功后刷新教师列表
      closeEditDialog() // 关闭弹框
    } else {
      ElMessage.error('专业修改失败')
    }
  } catch (error) {
    ElMessage.error('网络问题，修改失败')
  }
}

const fetchMajors = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/admin/getMajors/', // 假设这是获取通知的API
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    majors.value = response.data.majors
  } catch (error) {
    ElMessage.error('获取专业失败')
  }
}
onMounted(() => {
  fetchMajors()
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

.search-area .el-button {
  font-size: 14px;
  border-radius: 4px;
  padding: 8px 16px;
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

.el-table .el-button {
  padding: 6px 12px;
  border-radius: 4px;
}

.el-table .el-button[type='primary'] {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

/* 弹框样式 */
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

/* 响应式布局 */
@media (max-width: 768px) {
  .search-area {
    flex-direction: column;
    align-items: stretch;
  }

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
