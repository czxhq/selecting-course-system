<template>
  <div class="nav-container"></div>
  <NavigationBar1 :nav-items="navItems">
    <div
      style="
        margin-right: 30px;
        color: white;
        font-size: 18px;
        font-weight: 400;
      "
    >
      {{ '欢迎回来! ' + studentInfo.name }}
    </div>
    <div
      style="
        margin-right: 20px;
        color: white;
        font-size: 18px;
        font-weight: 400;
        cursor: pointer;
      "
      @click="openInfoDialog"
    >
      个人信息
    </div>
  </NavigationBar1>
  <router-view></router-view>
  <el-dialog
    title="个人信息"
    :model-value="isInfoDialogVisible"
    @update:model-value="isInfoDialogVisible = $event"
    width="50%"
    @close="resetInfoForm"
  >
    <el-form
      :model="newInfo"
      :rules="infoFormRules"
      ref="infoForm"
      label-width="100px"
    >
      <el-form-item label="电子邮箱" prop="email">
        <el-input v-model="newInfo.email" />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="newInfo.phone" />
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input v-model="newInfo.address" />
      </el-form-item>
    </el-form>

    <div slot="footer" class="dialog-footer">
      <el-button @click="sumbitInfo(infoForm)">关闭</el-button>
      <el-button type="primary" @click="logout">退出登录</el-button>
    </div>
  </el-dialog>
</template>
<script lang="ts" setup>
import { ref, reactive, onMounted, watch, onBeforeMount } from 'vue'
import {
  ElTable,
  ElTableColumn,
  ElPagination,
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElInputNumber,
  ElMessageBox,
  ElMessage,
  ElSelect,
  ElOption,
  type FormInstance
} from 'element-plus'
import axiosrequest from '@/services'
import type { AxiosRequestHeaders } from 'axios'
import { useRouter } from 'vue-router'
import { useTeacherStore } from '@/store/teacher'
import timeFormatTransfer from '@/utils/timeTransfer'
import CourseDetails from '../main/CourseDetails.vue'
import { ca } from 'element-plus/es/locales.mjs'
import { useToken } from '@/store/token'
const router = useRouter()
const routes: NavItem[] = [
  { name: '首页', to: '/main' },
  { name: '选课', to: '/main/courses' },
  { name: '帮助', to: '/main/help' }
]
const navItems = ref(routes)

const studentInfo = reactive({
  id: '',
  name: '',
  email: '',
  phone: '',
  address: ''
})

const fetchStudentInfo = async () => {
  try {
    const response = await axiosrequest.post({
      url: 'user/showStudentProfile/',
      data: {
        id: localStorage.getItem('id')
      },
      headers: {} as AxiosRequestHeaders
    })
    console.log(response.data)
    studentInfo.id = response.data.data.id
    studentInfo.name = response.data.data.name
    studentInfo.email = response.data.data.email
    studentInfo.phone = response.data.data.phone
    studentInfo.address = response.data.data.address
  } catch (error) {
    ElMessage.error('网络错误')
  }
}

const isInfoDialogVisible = ref(false)
const infoForm = ref<FormInstance>()
const newInfo = reactive({
  email: '',
  phone: '',
  address: ''
})

const infoFormRules = reactive({
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
})

const openInfoDialog = () => {
  isInfoDialogVisible.value = true
  newInfo.email = studentInfo.email
  newInfo.phone = studentInfo.phone
  newInfo.address = studentInfo.address
}

const resetInfoForm = () => {
  Object.assign(newInfo, {
    email: '',
    phone: '',
    address: ''
  })
}

const sumbitInfo = async (formEl: FormInstance | undefined) => {
  if (!formEl) {
    return
  }

  await formEl.validate((valid, fields) => {
    if (valid) {
      submitInfoNet()
    }
  })
}

const submitInfoNet = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/user/updateStudentProfile/',
      data: {
        id: localStorage.getItem('id'),
        email: newInfo.email,
        phone: newInfo.phone,
        address: newInfo.address
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    isInfoDialogVisible.value = false
    fetchStudentInfo() // 重新获取课程列表
  } catch (error) {
    ElMessage.error('网络错误') // 发布失败后弹窗提示
  }
}

const logout = () => {
  useToken().clearToken()
  useTeacherStore().clearTeacherId()
  router.push('/')
}

onMounted(() => {
  fetchStudentInfo()
})
</script>
<style lang="less" scoped>
.nav-container {
  height: 75px;
  background: linear-gradient(to right, #145a9f, #2c77c1, #145a9f);
  width: 100%;
}
</style>
