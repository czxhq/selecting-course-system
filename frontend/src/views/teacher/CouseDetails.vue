<template>
  <div class="course-detail-container">
    <div class="course-header">
      <h2>{{ course.courseName }}</h2>
      <el-table :data="courseInfo" border style="width: 100%">
        <el-table-column label="属性" prop="attribute" width="150" />
        <el-table-column label="内容" prop="content" />
      </el-table>
    </div>

    <!-- 课程描述 -->
    <div v-if="course.courseDetails" class="course-description">
      <h3>课程介绍</h3>
      <p>{{ course.courseDetails }}</p>
    </div>

    <!-- 常见问题 -->
    <div v-if="course.courseQnA.length > 0" class="course-qna">
      <h3>常见问题与答案</h3>
      <div v-for="(qa, index) in paginatedQnA" :key="index" class="qa-item">
        <p><strong>Q: </strong>{{ qa.question }}</p>
        <p><strong>A: </strong>{{ qa.answer }}</p>
      </div>

      <!-- 分页 -->
      <el-pagination
        :current-page="currentQnAPage"
        :page-size="3"
        :total="course.courseQnA.length"
        @current-change="handleQnAPageChange"
        layout="prev, pager, next"
      />
    </div>

    <!-- 待回答问题 -->
    <div v-if="tobeAnswered.length > 0" class="course-qna">
      <h3>待回答问题</h3>
      <div v-for="(qa, index) in paginatedTqA" :key="index" class="qa-item1">
        <p><strong>Q: </strong>{{ qa.question }}</p>
        <el-button @click="openAnswerDialog(qa.id)"> 回答问题 </el-button>
      </div>

      <!-- 分页 -->
      <el-pagination
        :current-page="currentTqAPage"
        :page-size="3"
        :total="tobeAnswered.length"
        @current-change="handleTqAPageChange"
        layout="prev, pager, next"
      />
    </div>

    <!-- 发布通知 -->
    <el-button type="primary" @click="openPublishNoticeDialog"
      >发布通知</el-button
    >

    <!-- 修改课程 -->
    <el-button type="primary" @click="openEditCourseDialog">修改课程</el-button>

    <!-- 返回按钮 -->
    <el-button @click="goBack" class="back-btn">返回课程列表</el-button>

    <!-- 发布通知 Dialog -->
    <el-dialog
      title="发布通知"
      :model-value="noticeDialogVisible"
      @update:model-value="noticeDialogVisible = $event"
    >
      <el-form
        :model="noticeForm"
        label-width="80px"
        :rules="noticeFormRules"
        ref="noticeRef"
      >
        <el-form-item label="通知标题" prop="title">
          <el-input
            v-model="noticeForm.title"
            placeholder="请输入通知标题"
            :rows="4"
          />
        </el-form-item>
        <el-form-item label="通知内容" prop="content">
          <el-input
            type="textarea"
            v-model="noticeForm.content"
            placeholder="请输入通知内容"
            :rows="4"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="noticeDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitNotice(noticeRef)"
          >确 定</el-button
        >
      </span>
    </el-dialog>

    <!-- 回答问题 Dialog -->
    <el-dialog
      title="回答问题"
      :model-value="answerDialogVisible"
      @close="resetAnswer"
    >
      <el-form
        :model="answerForm"
        label-width="80px"
        :rules="answerFormRules"
        ref="answerRef"
      >
        <el-form-item label="答案" prop="answer">
          <el-input v-model="answerForm.answer" type="textarea" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="answerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAnswer(answerRef)"
          >确 定</el-button
        >
      </div>
    </el-dialog>

    <!-- 编辑课程 Dialog -->
    <el-dialog
      title="修改课程"
      :model-value="editCourseDialogVisible"
      @update:model-value="editCourseDialogVisible = $event"
    >
      <el-form
        :model="editCourseForm"
        label-width="80px"
        :rules="courseFormRules"
        ref="courseRef"
      >
        <el-form-item label="课程名" prop="courseName">
          <el-input v-model="editCourseForm.courseName" />
        </el-form-item>
        <el-form-item label="上课时间" prop="time">
          <div class="classForm">
            <el-button type="primary" @click="addTimePeriod"
              >添加时间段</el-button
            >
            <div
              v-for="(item, index) in editCourseForm.time"
              :key="index"
              class="time-period-group"
            >
              星期：
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
        <el-form-item label="地点" prop="location">
          <el-input v-model="editCourseForm.location" />
        </el-form-item>
        <el-form-item label="课程容量" prop="capacity">
          <el-input-number v-model="editCourseForm.capacity" :min="1" />
        </el-form-item>
        <el-form-item label="课程性质" prop="type">
          <el-select
            v-model="editCourseForm.type"
            placeholder="请选择必修还是选修"
          >
            <el-option label="必修" value="必修" />
            <el-option label="选修" value="选修" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程类别" prop="category">
          <el-select
            v-model="editCourseForm.category"
            placeholder="请选择课程类型"
          >
            <el-option label="核心专业类" value="核心专业类" />
            <el-option label="一般专业类" value="一般专业类" />
            <el-option label="核心通识类" value="核心通识类" />
            <el-option label="一般通识类" value="一般通识类" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程详情" prop="courseDetails">
          <el-input
            type="textarea"
            v-model="editCourseForm.courseDetails"
            placeholder="请输入课程详情"
            :rows="4"
          />
        </el-form-item>
        <el-form-item label="课程学分" prop="credits">
          <el-input v-model="editCourseForm.credits" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editCourseDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitEditCourse(courseRef)"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <div v-if="students.length > 0" class="student-list">
      <h3>已选学生</h3>
      <el-table :data="paginatedStudents" border style="width: 100%">
        <el-table-column label="学号" prop="id" width="150" />
        <el-table-column label="姓名" prop="name" />
      </el-table>

      <!-- 分页 -->
      <el-pagination
        :current-page="currentStudentPage"
        :page-size="10"
        :total="students.length"
        @current-change="handleStudentPageChange"
        layout="prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue'
import axiosrequest from '@/services'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import type { AxiosRequestHeaders } from 'axios'
import timeFormatTransfer, { timesToObj } from '@/utils/timeTransfer'
interface timePeriods {
  weekDay: number | undefined
  startPeriod: number | undefined
  endPeriod: number | undefined
  startWeek: number | undefined
  endWeek: number | undefined
}
const route = useRoute()
const router = useRouter()

const course = ref<any>({
  courseName: '',
  teacher: '',
  location: '',
  time: [],
  type: '',
  category: '',
  capacity: '',
  courseDetails: '',
  teacherInfo: '',
  courseReview: [],
  courseQnA: [],
  credits: ''
})

const currentQnAPage = ref(1)
const currentTqAPage = ref(1)
const tobeAnswered = ref<any>([])
const pageSize = 3 // 每页展示的数量

const courseInfo = computed(() => [
  { attribute: '课程名', content: course.value.courseName },
  { attribute: '教师', content: course.value.teacher },
  { attribute: '地点', content: course.value.location },
  { attribute: '上课时间', content: timeFormatTransfer(course.value.time) },
  { attribute: '课程性质', content: course.value.type },
  { attribute: '课程类型', content: course.value.category },
  { attribute: '容量/已选', content: course.value.capacity },
  { attribute: '课程学分', content: course.value.credits }
])

// 表单状态
const editCourseDialogVisible = ref(false)
const noticeDialogVisible = ref(false)
const answerDialogVisible = ref(false)

const editCourseForm = ref({
  courseName: '',
  time: [] as timePeriods[],
  location: '',
  capacity: undefined,
  type: '',
  category: '',
  courseDetails: '',
  credits: ''
})

const students = ref([])

const courseRef = ref<FormInstance>()
const courseFormRules = reactive({
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
const noticeForm = ref({ title: '', content: '' })
const noticeRef = ref<FormInstance>()
const answerForm = reactive({ answer: '' })
const answerRef = ref<FormInstance>()
const currentQId = ref('0')
const answerFormRules = reactive({
  answer: [{ required: true, message: '请输入回答', trigger: 'blur' }]
})

const noticeFormRules = reactive({
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
})
// 获取课程详情
const getCourseDetail = async () => {
  const courseId = route.params.courseId as string
  try {
    const response = await axiosrequest.post({
      url: '/courses/get/',
      data: { courseId },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.data) {
      course.value = response.data.data
    }
  } catch (error) {
    ElMessage.error('获取课程详情失败')
  }
}

// 获取待解答问题
const getQuestions = async () => {
  const courseId = route.params.courseId as string
  try {
    const response = await axiosrequest.post({
      url: '/teacher/question/',
      data: { courseId },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    tobeAnswered.value = response.data.result
  } catch (error) {
    ElMessage.error('获取问题失败')
  }
}

// 重置表单

const resetAnswer = () => {
  Object.assign(answerForm, {
    answer: ''
  })
  currentQId.value = '0'
}

// 发布通知
const submitNotice = async (noticeRef: FormInstance | undefined) => {
  if (!noticeRef) {
    return
  }
  await noticeRef.validate((valid, fields) => {
    if (valid) {
      submitNoticeNet()
    }
  })
}

const submitNoticeNet = async () => {
  const courseId = route.params.courseId as string
  const { title, content } = noticeForm.value
  try {
    const response = await axiosrequest.post({
      url: '/teacher/notifications/',
      data: { courseId, title, content },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('通知发布成功')
      noticeDialogVisible.value = false
    } else {
      ElMessage.error('通知发布失败')
    }
  } catch (error) {
    ElMessage.error('通知发布失败')
  }
}

// 提交答案
const submitAnswer = async (answerRef: FormInstance | undefined) => {
  if (!answerRef) {
    return
  }

  await answerRef.validate((valid, fields) => {
    if (valid) {
      submitAnswerNet()
    }
  })
}

const submitAnswerNet = async () => {
  const { answer } = answerForm
  if (!answer.trim()) {
    ElMessage.warning('请输入答案')
    return
  }
  try {
    const response = await axiosrequest.post({
      url: '/teacher/answer/',
      data: { id: currentQId.value, answer },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('回答提交成功')
      answerDialogVisible.value = false
      await getQuestions()
      await getCourseDetail()
    } else {
      ElMessage.error('回答提交失败')
    }
  } catch (error) {
    ElMessage.error('回答提交失败')
  }
}

// 修改课程
const submitEditCourse = async (courseRef: FormInstance | undefined) => {
  if (!courseRef) {
    return
  }

  await courseRef.validate((valid, fields) => {
    if (valid) {
      submitEditCourseNet()
    }
  })
}

const submitEditCourseNet = async () => {
  const courseId = route.params.courseId as string
  try {
    const response = await axiosrequest.post({
      url: '/teacher/alterCourse/',
      data: {
        teacherId: localStorage.getItem('id'),
        courseId,
        courseName: editCourseForm.value.courseName,
        time: formatTimePeriods(),
        location: editCourseForm.value.location,
        capacity: editCourseForm.value.capacity,
        type: editCourseForm.value.type,
        category: editCourseForm.value.category,
        courseDetails: editCourseForm.value.courseDetails,
        credits: editCourseForm.value.credits
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    if (response.data.result === 'success') {
      ElMessage.success('课程修改成功')
      editCourseDialogVisible.value = false
      await getCourseDetail()
    } else {
      ElMessage.error('存在课程冲突')
    }
  } catch (error) {
    ElMessage.error('修改课程失败')
  }
}

const formatTimePeriods = () => {
  // 格式化时间段为字符串
  const timeFormat: string[] = []
  for (const item of editCourseForm.value.time) {
    timeFormat.push(
      `${item.weekDay} ${item.startPeriod}-${item.endPeriod} ${item.startWeek}-${item.endWeek}`
    )
  }
  return timeFormat
}

const addTimePeriod = () => {
  editCourseForm.value.time.push({
    weekDay: undefined,
    startPeriod: undefined,
    endPeriod: undefined,
    startWeek: undefined,
    endWeek: undefined
  })
}

const removeTimePeriod = (index: number) => {
  editCourseForm.value.time.splice(index, 1)
}

// 打开编辑课程对话框
const openEditCourseDialog = () => {
  editCourseForm.value = {
    courseName: course.value.courseName,
    time: timesToObj(course.value.time),
    location: course.value.location,
    capacity: course.value.capacity,
    type: course.value.type,
    category: course.value.category,
    courseDetails: course.value.courseDetails,
    credits: course.value.credits
  }
  editCourseDialogVisible.value = true
}

// 打开回答问题对话框
const openAnswerDialog = (questionId: string) => {
  Object.assign(answerForm, { answer: '' })
  currentQId.value = questionId
  answerDialogVisible.value = true
}

// 打开发布通知对话框
const openPublishNoticeDialog = () => {
  noticeForm.value = { title: '', content: '' }
  noticeDialogVisible.value = true
}

const goBack = () => {
  router.push('/teacher-page/')
}

const enrollStudents = async () => {
  const courseId = route.params.courseId as string
  try {
    const response = await axiosrequest.post({
      url: '/teacher/enrollStudents/',
      data: { courseId },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    students.value = response.data.data
  } catch (error) {
    ElMessage.error('网络出错，获取已选学生名单失败')
  }
}

const currentStudentPage = ref(1) // 当前学生分页页码
const pageStudentSize = 10 // 每页显示学生数量

// 计算分页后的学生数据
const paginatedStudents = computed(() => {
  const start = (currentStudentPage.value - 1) * pageStudentSize
  const end = start + pageStudentSize
  return students.value.slice(start, end) // 根据分页计算当前页显示的学生
})

// 处理学生列表分页切换
const handleStudentPageChange = (page: number) => {
  currentStudentPage.value = page
}

onMounted(() => {
  getCourseDetail()

  getQuestions()

  enrollStudents()
})

// 分页处理
const handleQnAPageChange = (page: number) => {
  currentQnAPage.value = page
}

const handleTqAPageChange = (page: number) => {
  currentTqAPage.value = page
}

const paginatedQnA = computed(() => {
  const start = (currentQnAPage.value - 1) * pageSize
  const end = start + pageSize
  return course.value.courseQnA.slice(start, end)
})

const paginatedTqA = computed(() => {
  const start = (currentTqAPage.value - 1) * pageSize
  const end = start + pageSize
  return tobeAnswered.value.slice(start, end)
})
</script>

<style scoped>
/* 全局样式 */
.course-detail-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.course-header h2 {
  font-size: 36px;
  color: #333;
  margin-bottom: 10px;
}

.course-header p {
  font-size: 18px;
  color: #666;
  margin: 5px 0;
}

h3 {
  font-size: 24px;
  color: #409eff;
  margin-bottom: 15px;
}

.course-description,
.teacher-info,
.course-reviews,
.course-qna {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: opacity 1s ease;
}

.review-item {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stars {
  display: inline-block;
  position: relative;
  font-size: 20px;
}

.star {
  color: #ffd700; /* 黄星 */
}

.empty {
  color: #dcdcdc; /* 灰星 */
}

.qa-item1 {
  background: #f9f9f9;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.qa-item {
  background: #f9f9f9;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.question-form {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.question-input {
  width: 300px;
}

.submit-btn {
  padding: 10px 20px;
}

.back-btn {
  margin-top: 30px;
  background-color: #f56c6c;
  color: white;
  width: 200px;
  margin: 0 auto;
}

.back-btn:hover {
  background-color: #e34343;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.stars {
  display: inline-block;
  position: relative;
  font-size: 20px;
}

.star {
  color: #ffd700; /* 黄星 */
}

.empty {
  color: #dcdcdc; /* 灰星 */
}

/* 分页样式 */
.el-pagination {
  margin-top: 20px;
  text-align: center;
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

.student-list {
  margin-top: 20px;
}

.student-list h3 {
  font-size: 24px;
  color: #409eff;
  margin-bottom: 15px;
}
</style>
