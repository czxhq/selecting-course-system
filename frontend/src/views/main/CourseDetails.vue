<template>
  <div class="course-detail-container">
    <!-- 课程头部及详情部分保持不变 -->
    <div class="course-header">
      <h2>{{ course.courseName }}</h2>
      <el-table :data="courseInfo" border style="width: 100%">
        <el-table-column label="属性" prop="attribute" width="150" />
        <el-table-column label="内容" prop="content" />
      </el-table>
    </div>

    <transition
      name="fade"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div v-if="course.courseDetails" class="course-description">
        <h3>课程介绍</h3>
        <p>{{ course.courseDetails }}</p>
      </div>
    </transition>

    <transition
      name="fade"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div v-if="course.teacherInfo" class="teacher-info">
        <h3>教师介绍</h3>
        <p>{{ course.teacherInfo }}</p>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="course.courseReview.length > 0" class="course-reviews">
        <h3>课程评价</h3>
        <div
          v-for="(review, index) in paginatedReviews"
          :key="index"
          class="review-item"
        >
          <p>
            <strong>{{ review.student }}：</strong>评分:
            <span class="stars">
              <template v-for="i in review.rating" :key="i">
                <span class="star">&#9733;</span>
              </template>
              <template v-for="i in 5 - review.rating" :key="i">
                <span class="star empty">&#9733;</span>
              </template>
            </span>
          </p>
          <p>{{ review.comment }}</p>
        </div>
        <el-pagination
          :current-page="currentReviewPage"
          :page-size="3"
          :total="course.courseReview.length"
          @current-change="handleReviewPageChange"
          layout="prev, pager, next"
        />
      </div>
    </transition>

    <transition name="fade">
      <div v-if="course.courseQnA.length > 0" class="course-qna">
        <h3>常见问题与答案</h3>
        <div v-for="(qa, index) in paginatedQnA" :key="index" class="qa-item">
          <p><strong>Q: </strong>{{ qa.question }}</p>
          <p><strong>A: </strong>{{ qa.answer }}</p>
        </div>
        <el-pagination
          :current-page="currentQnAPage"
          :page-size="3"
          :total="course.courseQnA.length"
          @current-change="handleQnAPageChange"
          layout="prev, pager, next"
        />
      </div>
    </transition>

    <!-- 提问部分 -->
    <transition name="fade">
      <div class="question-form">
        <el-input
          v-model="newQuestion"
          placeholder="提问..."
          class="question-input"
        ></el-input>
        <el-button type="primary" @click="submitQuestion" class="submit-btn"
          >提交问题</el-button
        >
      </div>
    </transition>

    <!-- 评价部分 -->
    <transition name="fade">
      <div class="review-form">
        <el-rate v-model="rating" class="rating" :max="5" show-text></el-rate>
        <el-input
          v-model="comment"
          type="textarea"
          placeholder="请输入评价..."
          :rows="4"
        ></el-input>
        <el-button type="primary" @click="submitReview" class="submit-btn"
          >提交评价</el-button
        >
      </div>
    </transition>

    <!-- 返回按钮 -->
    <el-button @click="goBack" class="back-btn">返回课程列表</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axiosrequest from '@/services'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AxiosRequestHeaders } from 'axios'
import timeFormatTransfer from '@/utils/timeTransfer'

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
  courseQnA: []
})

const newQuestion = ref('')
const rating = ref(0) // 评分
const comment = ref('') // 评价内容
const currentReviewPage = ref(1) // 当前课程评价分页页码
const currentQnAPage = ref(1) // 当前常见问题分页页码

const pageSize = 3 // 每页展示的数量

const courseInfo = computed(() => [
  { attribute: '课程名', content: course.value.courseName },
  { attribute: '教师', content: course.value.teacher },
  { attribute: '地点', content: course.value.location },
  { attribute: '上课时间', content: course.value.time.join(', ') },
  { attribute: '课程性质', content: course.value.type },
  { attribute: '课程类型', content: course.value.category },
  { attribute: '容量/已选', content: course.value.capacity }
])

const getCourseDetail = async () => {
  const courseId = route.params.courseId as string
  try {
    const response = await axiosrequest.post({
      url: 'courses/get/',
      data: { courseId },
      headers: { 'Content-Type': 'application/json' } as AxiosRequestHeaders
    })
    course.value = response.data.data
    course.value.time = [timeFormatTransfer(course.value.time)]
  } catch (error) {
    ElMessage.error('获取课程详情失败')
  }
}

const submitQuestion = async () => {
  if (!newQuestion.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  const courseId = route.params.courseId as string
  const question = newQuestion.value
  try {
    const response = await axiosrequest.post({
      url: 'courses/question/',
      data: { courseId, question },
      headers: { 'Content-Type': 'application/json' } as AxiosRequestHeaders
    })

    if (response.data.result === 'success') {
      newQuestion.value = ''
      await getCourseDetail()
      ElMessage.success('问题提交成功')
    } else {
      ElMessage.error('问题提交失败')
    }
  } catch (error) {
    ElMessage.error('提交失败')
  }
}

const submitReview = async () => {
  if (rating.value === 0 || !comment.value.trim()) {
    ElMessage.warning('请输入评分和评价')
    return
  }

  const courseId = route.params.courseId as string
  const studentId = localStorage.getItem('id') // 假设这里有获取学生ID的方法
  try {
    const response = await axiosrequest.post({
      url: '/courses/addReview/',
      data: {
        courseId,
        studentId,
        rating: rating.value,
        comment: comment.value
      },
      headers: { 'Content-Type': 'application/json' } as AxiosRequestHeaders
    })

    if (response.data.result === 'success') {
      rating.value = 0
      comment.value = ''
      await getCourseDetail()
      ElMessage.success('评价提交成功')
    } else {
      ElMessage.error('评价提交失败')
    }
  } catch (error) {
    ElMessage.error('提交评价失败')
  }
}

const goBack = () => {
  router.push('/main/courses')
}

onMounted(() => {
  getCourseDetail()
})

const handleReviewPageChange = (page: number) => {
  currentReviewPage.value = page
}

const handleQnAPageChange = (page: number) => {
  currentQnAPage.value = page
}

const paginatedReviews = computed(() => {
  const start = (currentReviewPage.value - 1) * pageSize
  const end = start + pageSize
  return course.value.courseReview.slice(start, end)
})

const paginatedQnA = computed(() => {
  const start = (currentQnAPage.value - 1) * pageSize
  const end = start + pageSize
  return course.value.courseQnA.slice(start, end)
})

const beforeEnter = (el: any) => {
  el.style.opacity = 0
}
const enter = (el: any, done: any) => {
  el.offsetHeight
  el.style.transition = 'opacity 1s ease'
  el.style.opacity = 1
  done()
}
const leave = (el: any, done: any) => {
  el.style.transition = 'opacity 1s ease'
  el.style.opacity = 0
  done()
}
</script>

<style scoped>
/* 样式保持不变 */
.review-form {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.rating {
  margin-bottom: 10px;
}

.submit-btn {
  padding: 10px 20px;
}
</style>

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
</style>
