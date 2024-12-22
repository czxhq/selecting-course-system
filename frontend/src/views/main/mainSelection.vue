<template>
  <div class="selected-courses">
    <h2>已选课程</h2>

    <!-- 课程表 -->
    <el-table
      :data="paginatedCourses"
      style="width: 100%"
      class="courses-table"
    >
      <el-table-column label="课程名称" prop="courseName" width="200" />
      <el-table-column label="教师" prop="teacher" width="150" />
      <el-table-column label="地点" prop="location" width="150" />
      <el-table-column label="时间" prop="time" width="250" />
      <el-table-column label="性质" prop="type" width="100" />
      <el-table-column label="类型" prop="category" width="100" />
      <el-table-column label="容量/已选" prop="capacity" width="150" />
      <el-table-column label="学分" prop="credits" width="100" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button
            @click="openCancelDialog(row)"
            type="danger"
            size="small"
            class="cancel-btn"
            >退课</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total="courses.length"
      @current-change="handlePageChange"
      layout="prev, pager, next"
      class="pagination"
    />

    <!-- 退课确认弹窗 -->
    <el-dialog
      :model-value="dialogVisible"
      title="确认退课"
      width="400px"
      @update:model-value="dialogVisible = $event"
      class="cancel-dialog"
    >
      <p>您确认要退选课程《{{ selectedCourse?.courseName }}》吗？</p>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCancel">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axiosrequest from '@/services'
import type { AxiosRequestHeaders } from 'axios'
import {
  ElTable,
  ElTableColumn,
  ElButton,
  ElDialog,
  ElPagination,
  ElMessage
} from 'element-plus'
import { useMainPageStore } from '@/store/mainPage'
import timeFormatTransfer from '@/utils/timeTransfer'

// 定义课程类型
type Course = {
  courseId: string
  courseName: string
  teacher: string
  location: string
  time: string | string[]
  type: string
  category: string
  capacity: string
  credits: string
}

// 定义响应数据
type CourseResponse = {
  courses: Course[]
}

// 定义组件内状态
const store = useMainPageStore()
const courses = ref<Course[]>([]) // 存储已选课程
const dialogVisible = ref(false) // 控制确认弹窗显示
const selectedCourse = ref<Course | null>(null) // 当前选中的课程
const currentPage = ref(1) // 当前分页
const pageSize = 10 // 每页显示的课程数

// 获取已选课程数据
const fetchSelectedCourses = async (studentId: string) => {
  axiosrequest
    .post({
      url: 'home/courseSelect/',
      data: {
        studentId: studentId
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    .then((response) => {
      courses.value = response.data.courses
      for (const course of courses.value) {
        course.time = timeFormatTransfer(course.time as string[])
      }
    })
    .catch((error) => {
      ElMessage.error('获取课程信息失败:', error)
    })
}

// 打开退课确认框
const openCancelDialog = (course: Course) => {
  selectedCourse.value = course
  dialogVisible.value = true
}

// 确认退课
const confirmCancel = async () => {
  if (!selectedCourse.value) return
  axiosrequest
    .post({
      url: 'courses/cancelCourse/',
      data: {
        courseId: selectedCourse.value?.courseId,
        studentId: localStorage.getItem('id')
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    .then((response) => {
      if (response.data.result === 'success') {
        // 退课成功，从已选课程中移除该课程
        courses.value = courses.value.filter(
          (course) => course.courseId !== selectedCourse.value?.courseId
        )
        dialogVisible.value = false
        selectedCourse.value = null
        emit('change', '课程发生变化')
      } else {
        ElMessage.error('退课失败')
      }
    })
    .catch((error) => {
      ElMessage.error('退课失败:', error)
    })
}

onMounted(() => {
  fetchSelectedCourses(localStorage.getItem('id') as string)
})

import { defineEmits } from 'vue'

// 定义事件，事件名称为 'myEvent'，可以传递一个字符串类型的参数
const emit = defineEmits<{
  (event: 'change', message: string): void
}>()

// 计算分页后的课程数据
const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  const courseList = courses.value.slice(start, end)
  return courseList
})

// 处理分页变化
const handlePageChange = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped>
.selected-courses {
  padding: 20px;
  background-color: #f4f7fc;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 26px;
  color: #333;
  margin-bottom: 20px;
}

.courses-table {
  border-collapse: collapse;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  border-radius: 8px;
}

.el-table th,
.el-table td {
  text-align: center; /* 居中对齐 */
  padding: 12px 15px; /* 表格内边距 */
  border: 1px solid #e4e7ed; /* 表格单元格边框 */
}

.el-table th {
  background-color: #f5f7fa;
  color: #4d4d4d;
  font-weight: bold;
}

.el-table .cell {
  font-size: 14px;
  color: #555;
}

.cancel-btn {
  transition:
    background-color 0.3s,
    transform 0.3s;
}

.cancel-btn:hover {
  background-color: #d9534f;
  transform: scale(1.05);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 0;
}

.pagination .el-pagination__total {
  margin-right: 15px;
}

.pagination .el-pagination__button,
.pagination .el-pagination__prev,
.pagination .el-pagination__next {
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  background-color: #f1f1f1;
  color: #333;
}

.pagination .el-pagination__button:hover,
.pagination .el-pagination__prev:hover,
.pagination .el-pagination__next:hover {
  background-color: #b0c4de;
  color: #1e3a8a;
}

.pagination .el-pagination__active {
  background-color: #3b82f6;
  color: white;
}

.cancel-dialog {
  transition: opacity 0.3s ease-in-out;
  border-radius: 10px;
}

.dialog-footer {
  text-align: right;
}

.el-button--primary {
  background-color: #4caf50;
  border-color: #4caf50;
  transition: background-color 0.3s;
}

.el-button--primary:hover {
  background-color: #45a049;
}
</style>
