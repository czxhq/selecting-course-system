<template>
  <div class="root">
    <div class="nav-container"></div>
    <NavigationBar1 :nav-items="[]">
      <div
        style="
          margin-right: 30px;
          color: white;
          font-size: 18px;
          font-weight: 400;
        "
      >
        {{ '欢迎回来! ' + teacherInfo.name }}
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
    <div class="main-container">
      <div class="section1">
        <div class="time-section">
          <h3 style="font-size: 18px; font-weight: 700; margin-bottom: 20px">
            我的课表
          </h3>
          <TimeTable :courses="courses" :key="renderkey"></TimeTable>
        </div>
        <div class="right-section">
          <div class="message-section">
            <MessageCenter
              :url="'/home/messages/'"
              :id="teacherId"
              style="height: 462px"
            ></MessageCenter>
          </div>
          <div class="time-select">
            <h3 style="font-size: 28px; font-weight: 700">日程安排</h3>
            <TimeSelect :courses="courses"></TimeSelect>
          </div>
        </div>
      </div>
      <div class="class-container">
        <h3 style="font-size: 24px; font-weight: 700">课程管理</h3>
        <el-button
          type="primary"
          @click="openPublishDialog"
          style="width: 70px; margin-top: 15px"
          >发布课程</el-button
        >

        <!-- 课程列表表格 -->
        <el-table
          :data="timeFormatcourses"
          style="width: 100%; margin-top: 20px"
          stripe
        >
          <el-table-column label="课程名称" prop="courseName" width="180" />
          <el-table-column label="上课地点" prop="location" width="180" />
          <el-table-column label="上课时间" prop="time" />
          <el-table-column label="操作" width="200">
            <template v-slot="scope">
              <el-button type="text" @click="viewCourseDetails(scope.row)"
                >查看详情</el-button
              >
              <el-button type="text" @click="confirmDeleteCourse(scope.row)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :total="totalCourses"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />

        <!-- 发布课程弹窗 -->
        <el-dialog
          title="发布课程"
          :model-value="isPublishDialogVisible"
          @update:model-value="isPublishDialogVisible = $event"
          width="50%"
          @close="resetForm"
        >
          <el-form
            :model="newCourse"
            :rules="formRules"
            ref="courseForm"
            label-width="100px"
          >
            <el-form-item label="课程名称" prop="courseName">
              <el-input v-model="newCourse.courseName" />
            </el-form-item>
            <el-form-item label="上课时间" prop="time">
              <div class="classForm">
                <el-button type="primary" @click="addTimePeriod"
                  >添加时间段</el-button
                >
                <div
                  v-for="(item, index) in newCourse.time"
                  :key="index"
                  class="time-period-group"
                >
                  <el-select
                    v-model="item.weekDay"
                    placeholder="选择周几"
                    :clearable="true"
                  >
                    <el-option label="周一" value="1" />
                    <el-option label="周二" value="2" />
                    <el-option label="周三" value="3" />
                    <el-option label="周四" value="4" />
                    <el-option label="周五" value="5" />
                    <el-option label="周六" value="6" />
                    <el-option label="周日" value="7" />
                  </el-select>
                  开始节数：
                  <el-input-number
                    v-model="item.startPeriod"
                    :min="1"
                    :max="14"
                    label="开始节数"
                  />
                  <br />
                  结束节数：
                  <el-input-number
                    v-model="item.endPeriod"
                    :min="1"
                    :max="14"
                    label="结束节数"
                  />
                  <br />
                  开始周数：
                  <el-input-number
                    v-model="item.startWeek"
                    :min="1"
                    :max="16"
                    label="开始周数"
                  />
                  <br />
                  结束周数：
                  <el-input-number
                    v-model="item.endWeek"
                    :min="1"
                    :max="16"
                    label="结束周数"
                  />
                  <br />
                  <el-button type="danger" @click="removeTimePeriod(index)"
                    >删除</el-button
                  >
                </div>
              </div>
            </el-form-item>
            <el-form-item label="上课地点" prop="location">
              <el-input v-model="newCourse.location" />
            </el-form-item>
            <el-form-item label="课程容量" prop="capacity">
              <el-input-number v-model="newCourse.capacity" :min="1" />
            </el-form-item>
            <el-form-item label="课程性质" prop="type">
              <el-select
                v-model="newCourse.type"
                placeholder="请选择必修还是选修"
              >
                <el-option label="必修" value="必修" />
                <el-option label="选修" value="选修" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程类别" prop="category">
              <el-select
                v-model="newCourse.category"
                placeholder="请选择课程类型"
              >
                <el-option label="核心专业类" value="核心专业类" />
                <el-option label="一般专业类" value="一般专业类" />
                <el-option label="核心通识类" value="核心通识类" />
                <el-option label="一般通识类" value="一般通识类" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程详情" prop="courseDetails">
              <el-input type="textarea" v-model="newCourse.courseDetails" />
            </el-form-item>
            <el-form-item label="课程学分" prop="credits">
              <el-input v-model="newCourse.credits" />
            </el-form-item>
          </el-form>

          <div slot="footer" class="dialog-footer">
            <el-button @click="isPublishDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmPublishCourse(courseForm)"
              >发布课程</el-button
            >
          </div>
        </el-dialog>

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
            <el-form-item label="教师介绍" prop="teacherInfo">
              <el-input v-model="newInfo.teacherInfo" type="textarea" />
            </el-form-item>
          </el-form>

          <div slot="footer" class="dialog-footer">
            <el-button @click="sumbitInfo(infoForm)">关闭</el-button>
            <el-button type="primary" @click="logout">退出登录</el-button>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

interface timePeriods {
  weekDay: number | undefined
  startPeriod: number | undefined
  endPeriod: number | undefined
  startWeek: number | undefined
  endWeek: number | undefined
}

// 课程数据
const teacherId = localStorage.getItem('id') as string
const courses = ref<any[]>([])
const timeFormatcourses = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(5)
const totalCourses = ref(0)
const courseForm = ref<FormInstance>()
const router = useRouter()
const renderkey = ref(0)
// 发布课程表单弹窗相关
const isPublishDialogVisible = ref(false)
const newCourse = reactive({
  courseName: '',
  time: [] as timePeriods[],
  location: '',
  capacity: 0,
  type: '',
  category: '',
  courseDetails: '',
  credits: ''
})
const formRules = reactive({
  courseName: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  time: [{ required: true, message: '请输入课程时间', trigger: 'blur' }],
  location: [{ required: true, message: '请输入上课地点', trigger: 'blur' }],
  capacity: [{ required: true, message: '请输入课程容量', trigger: 'blur' }],
  type: [{ required: true, message: '请输入课程性质', trigger: 'blur' }],
  category: [{ required: true, message: '请输入课程类别', trigger: 'blur' }],
  courseDetails: [
    { required: true, message: '请输入课程详情', trigger: 'blur' }
  ],
  credits: [{ required: true, message: '请输入课程学分', trigger: 'blur' }]
})

watch(courses, (newValue) => {
  timeFormatcourses.value = []
  for (const course of newValue) {
    timeFormatcourses.value.push({
      courseId: course.courseId,
      courseName: course.courseName,
      time: timeFormatTransfer(course.time),
      location: course.location,
      capacity: course.capacity,
      category: course.category,
      courseDetails: course.courseDetails,
      credits: course.credits
    })
  }
})

// 获取教师课程信息
const fetchCourses = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/home/teacherCourses/',
      data: {
        TeacherId: localStorage.getItem('id') // 假设教师ID为 teacher123
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    courses.value = response.data.data.courses
    renderkey.value++
    for (const course of courses.value) {
      timeFormatcourses.value.push({
        courseId: course.courseId,
        courseName: course.courseName,
        time: timeFormatTransfer(course.time),
        location: course.location,
        capacity: course.capacity,
        category: course.category,
        courseDetails: course.courseDetails,
        credits: course.credits
      })
    }
    totalCourses.value = courses.value.length
  } catch (error) {
    ElMessage.error('获取课程信息失败:')
  }
}

// 页码变化处理
const handlePageChange = (page: number) => {
  currentPage.value = page
}

// 发布课程功能
const openPublishDialog = () => {
  isPublishDialogVisible.value = true
}

const resetForm = () => {
  Object.assign(newCourse, {
    courseName: '',
    time: [],
    location: '',
    capacity: 0,
    type: '',
    category: '',
    courseDetails: '',
    credits: ''
  })
}

// 发布课程确认操作
const confirmPublishCourse = async (formEl: FormInstance | undefined) => {
  if (!formEl) {
    return
  }

  await formEl.validate((valid, fields) => {
    if (valid) {
      confirmNet()
    }
  })
}

const confirmNet = async () => {
  try {
    const response = await axiosrequest.post({
      url: 'teacher/publishCourse/',
      data: {
        teacherId: localStorage.getItem('id'),
        courseName: newCourse.courseName,
        time: formatTimePeriods(),
        location: newCourse.location,
        capacity: newCourse.capacity,
        type: newCourse.type,
        category: newCourse.category,
        courseDetails: newCourse.courseDetails,
        credits: newCourse.credits
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    isPublishDialogVisible.value = false
    fetchCourses() // 重新获取课程列表
    if (response.data.result === 'success') {
      ElMessage.success('课程发布成功！') // 发布成功后弹窗提示
    } else {
      ElMessage.error('课程发生冲突')
    }
  } catch (error) {
    ElMessage.error('发布课程失败，请稍后重试！') // 发布失败后弹窗提示
  }
}

const addTimePeriod = () => {
  newCourse.time.push({
    weekDay: undefined,
    startPeriod: undefined,
    endPeriod: undefined,
    startWeek: undefined,
    endWeek: undefined
  })
}

const removeTimePeriod = (index: number) => {
  newCourse.time.splice(index, 1)
}

// 删除课程功能
const confirmDeleteCourse = (course: any) => {
  ElMessageBox.confirm('您确定要删除这门课程吗？', '删除确认', {
    confirmButtonText: '删除',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await axiosrequest.post({
        url: 'teacher/deleteCourse/',
        data: {
          courseId: course.courseId
        },
        headers: {
          'Content-Type': 'application/json'
        } as AxiosRequestHeaders
      })
      fetchCourses() // 删除后刷新课程列表
      ElMessage.success('课程删除成功！') // 删除成功后弹窗提示
    } catch (error) {
      ElMessage.error('删除课程失败，请稍后重试！') // 删除失败后弹窗提示
    }
  })
}

// 查看课程详情（暂时保留）
const viewCourseDetails = (course: any) => {
  router.push({ name: 'CourseDetail', params: { courseId: course.courseId } })
}

const formatTimePeriods = () => {
  // 格式化时间段为字符串
  const timeFormat: string[] = []
  for (const item of newCourse.time) {
    timeFormat.push(
      `${item.weekDay} ${item.startPeriod}-${item.endPeriod} ${item.startWeek}-${item.endWeek}`
    )
  }
  return timeFormat
}

//教师信息获取
const teacherInfo = reactive({
  id: '',
  name: '',
  email: '',
  phone: '',
  address: '',
  intro: ''
})

const fetchTeacherInfo = async () => {
  try {
    const response = await axiosrequest.post({
      url: 'user/showTeacherProfile/',
      data: {
        id: localStorage.getItem('id')
      },
      headers: {} as AxiosRequestHeaders
    })
    teacherInfo.id = response.data.data.id
    teacherInfo.name = response.data.data.name
    teacherInfo.email = response.data.data.email
    teacherInfo.phone = response.data.data.phone
    teacherInfo.address = response.data.data.address
    teacherInfo.intro = response.data.data.intro
  } catch (error) {
    ElMessage.error('网络错误')
  }
}

const isInfoDialogVisible = ref(false)
const infoForm = ref<FormInstance>()
const newInfo = reactive({
  email: '',
  phone: '',
  address: '',
  teacherInfo: ''
})

const infoFormRules = reactive({
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }],
  teacherInfo: [{ required: true, message: '请输入教师介绍', trigger: 'blur' }]
})

const openInfoDialog = () => {
  isInfoDialogVisible.value = true
  newInfo.email = teacherInfo.email
  newInfo.phone = teacherInfo.phone
  newInfo.address = teacherInfo.address
  newInfo.teacherInfo = teacherInfo.intro
}

const resetInfoForm = () => {
  Object.assign(newInfo, {
    email: '',
    phone: '',
    address: '',
    teacherInfo: ''
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
      url: '/user/updateTeacherProfile/',
      data: {
        id: localStorage.getItem('id'),
        email: newInfo.email,
        phone: newInfo.phone,
        address: newInfo.address,
        teacherInfo: newInfo.teacherInfo
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    isInfoDialogVisible.value = false
    fetchTeacherInfo() // 重新获取课程列表
  } catch (error) {
    ElMessage.error('网络错误') // 发布失败后弹窗提示
  }
}

const logout = () => {
  useToken().clearToken()
  useTeacherStore().clearTeacherId()
  router.push('/')
}

// 页面加载时获取课程信息
onMounted(() => {
  fetchCourses()
  fetchTeacherInfo()
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.root {
  background-color: rgb(240, 245, 255);
}

.nav-container {
  height: 75px;
  background: linear-gradient(to right, #145a9f, #2c77c1, #145a9f);
  width: 100%;
}

.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.class-container {
  background-color: white;
  border-radius: 30px;
  padding: 40px 30px;
  width: 85%;
  display: flex;
  flex-direction: column;
}

.section1 {
  display: flex;
  flex-wrap: wrap;
  padding: 40px 30px;
}

.time-section {
  width: 68%;
  background-color: white;
  border-radius: 30px;
  padding: 30px 30px;
}

.right-section {
  display: flex;
  flex-direction: column;
  width: 30%;
  height: 924px;
}

.message-section {
  margin-top: -20px;
  margin-left: 30px;
  height: 60%;
  flex-grow: 1;
}

.time-select {
  background-color: white;
  border-radius: 30px;
  margin-top: 35px;
  margin-left: 30px;
  padding: 30px 20px;
  height: 50%;
  overflow-y: auto;
}

.message-center-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
}

.course-table-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.course-list {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.time-period-group {
  margin-top: 20px; /* 使每个时间段之间的间隔稍微大一点 */
  padding: 15px;
  border: 1px solid #ddd; /* 给每个时间段添加边框 */
  border-radius: 8px; /* 圆角效果 */
  background-color: #f9f9f9; /* 背景色稍微柔和 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 给每个时间段加上微弱阴影 */
}

.time-period-group el-select,
.time-period-group el-input-number {
  width: 100%;
  margin-bottom: 10px; /* 给每个输入框下面添加间距 */
}

.time-period-group el-button {
  margin-top: 10px; /* 给删除按钮添加顶部间距 */
  align-self: flex-start; /* 按钮靠左对齐 */
}

.time-period-group .el-row {
  display: flex;
  justify-content: space-between; /* 水平分布各个输入框 */
  margin-bottom: 15px;
}

.time-period-group .el-col {
  display: flex;
  align-items: center;
  gap: 10px; /* 增加输入框之间的间距 */
}

.time-period-group .el-button {
  padding: 5px 15px;
  font-size: 14px;
  border-radius: 5px;
  background-color: #ff4d4f; /* 红色按钮 */
  color: white;
  transition: background-color 0.3s ease;
}

.time-period-group .el-button:hover {
  background-color: #e63946; /* 悬停时更深的红色 */
}

/* 样式细节 */
.el-select .el-input {
  padding: 5px 10px;
  font-size: 14px;
}

.el-input-number .el-input__inner {
  padding: 5px 10px;
  font-size: 14px;
}

.classForm {
  display: flex;
  flex-direction: column;
}
</style>
