<template>
  <div class="container">
    <!-- 搜索框 -->
    <div class="search-box">
      <el-input
        v-model="searchTerm"
        placeholder="请输入课程名或教师名"
        class="search-input"
        prefix-icon="el-icon-search"
        clearable
        size="small"
      ></el-input>

      <el-select
        v-model="searchType"
        placeholder="搜索类型"
        class="search-select"
        size="small"
      >
        <el-option label="按课程名搜索" value="0" style="text-align: center" />
        <el-option label="按教师名搜索" value="1" style="text-align: center" />
      </el-select>

      <el-checkbox
        v-model="hideConflicts"
        class="conflict-checkbox"
        size="small"
      >
        隐藏冲突课程
      </el-checkbox>
      <!-- 搜索和返回按钮换行 -->
      <div class="action-buttons">
        <el-button @click="searchCourses" type="primary" class="search-btn">
          搜索
        </el-button>
        <el-button @click="clearSearch" type="default" class="clear-btn">
          返回
        </el-button>
      </div>
    </div>

    <!-- 显示课程表格 -->
    <el-table :data="paginatedCourses" border class="course-table">
      <el-table-column label="课程ID" prop="courseId" width="100" />
      <el-table-column label="课程名" prop="courseName" width="150">
        <template #default="{ row }">
          <span
            v-if="isLongText(row.courseName)"
            class="ellipsis"
            :title="row.courseName"
          >
            {{ row.courseName }}
          </span>
          <span v-else>{{ row.courseName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="教师" prop="teacher" width="150">
        <template #default="{ row }">
          <span
            v-if="isLongText(row.teacher)"
            class="ellipsis"
            :title="row.teacher"
          >
            {{ row.teacher }}
          </span>
          <span v-else>{{ row.teacher }}</span>
        </template>
      </el-table-column>
      <el-table-column label="地点" prop="location" width="90">
        <template #default="{ row }">
          <span
            v-if="isLongText(row.location)"
            class="ellipsis"
            :title="row.location"
          >
            {{ row.location }}
          </span>
          <span v-else>{{ row.location }}</span>
        </template>
      </el-table-column>
      <el-table-column label="时间" prop="time" width="180" />
      <el-table-column label="性质" prop="type" width="60" />
      <el-table-column label="类别" prop="category" width="100" />
      <el-table-column label="容量/已选" prop="capacity" width="90" />
      <el-table-column label="学分" prop="credits" width="60" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="viewCourseDetail(row.courseId)"
            >查看详情</el-button
          >
          <el-button
            size="small"
            type="primary"
            :disabled="row.capacity.split('/')[1] >= row.capacity.split('/')[0]"
            @click="selectCourse(row.courseId)"
            v-if="!row.isSelect"
          >
            选择课程
          </el-button>
          <el-button size="small" type="primary" :disabled="true" v-else>
            已选课程
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div class="pagination-container">
      <el-pagination
        v-if="totalCourses > 0"
        :page-size="pageSize"
        :current-page="currentPage"
        :total="totalCourses"
        layout="total, prev, pager, next, jumper"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import axiosrequest from '@/services'
import { ElMessage } from 'element-plus'
import type { AxiosRequestHeaders } from 'axios'
import { useMainPageStore } from '@/store/mainPage'
import { useRouter } from 'vue-router'
import timeFormatTransfer from '@/utils/timeTransfer'

interface Course {
  isSelect: boolean
  courseId: string
  courseName: string
  teacher: string
  location: string
  time: string[] | string
  type: string
  category: string
  capacity: string
  credits: string
}

const courses = ref<Course[]>([]) // 存储所有课程
const pageSize = ref(15) // 每页显示15条课程
const currentPage = ref(1) // 当前页
const totalCourses = ref(0) // 总课程数量
const store = useMainPageStore()
const router = useRouter()
// 搜索相关状态
const searchTerm = ref('') // 搜索关键词
const searchType = ref(undefined) // 搜索类型（按课程名搜索: 0，按教师名搜索: 1）
const hideConflicts = ref(true) // 是否隐藏冲突课程

// 用来保存原始课程数据
const allCourses = ref<Course[]>([])

// 请求获取课程数据
const getCourses = async () => {
  try {
    const response = await axiosrequest.post({
      url: '/courses/allCourse/',
      data: {
        studentId: localStorage.getItem('id'),
        'hide-conflict': hideConflicts.value
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    allCourses.value = response.data.courses
    courses.value = [...allCourses.value]
    for (const course of courses.value) {
      course.time = timeFormatTransfer(course.time as string[])
    }
    totalCourses.value = courses.value.length
  } catch (error) {
    ElMessage.error('获取课程失败！')
  }
}

// 搜索课程
const searchCourses = async () => {
  if (!searchTerm.value.trim()) {
    getCourses()
    return
  }

  if (!searchType.value) {
    ElMessage.warning('请输入搜索类型')
    return
  }

  try {
    const response = await axiosrequest.post({
      url: '/courses/search/', // 搜索接口
      data: {
        studentId: localStorage.getItem('id'),
        query: searchTerm.value,
        type: searchType.value,
        'hide-conflict': hideConflicts.value
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })

    if (response.data && response.data.courses) {
      courses.value = response.data.courses
      totalCourses.value = courses.value.length
    } else {
      ElMessage.warning('没有找到相关课程')
    }
  } catch (error) {
    ElMessage.error('搜索失败!')
  }
}

// 清除搜索，恢复到初始的课程列表
const clearSearch = () => {
  searchTerm.value = ''
  searchType.value = undefined
  hideConflicts.value = false
  courses.value = [...allCourses.value] // 恢复原始课程数据
  totalCourses.value = allCourses.value.length
}

// 判断单元格内容是否过长
const isLongText = (text: string): boolean => {
  return text.length > 20 // 假设超过20个字符的文本显示省略号
}

// 查看课程详情
const viewCourseDetail = (courseId: string) => {
  router.push({ name: 'course-detail', params: { courseId } })
}

// 选择课程
const selectCourse = async (courseId: string) => {
  const studentId = localStorage.getItem('id')
  try {
    await axiosrequest
      .post({
        url: 'courses/selectCourse/',
        data: { courseId, studentId },
        headers: { 'Content-Type': 'application/json' } as AxiosRequestHeaders
      })
      .then((response) => {
        if (response.data.result === 'success') {
          ElMessage.success('课程选择成功！')
          searchCourses()
        } else {
          ElMessage.error('课程选择失败！')
        }
      })
  } catch (error) {
    ElMessage.error('网络错误，课程选择失败')
  }
}

// 页面加载时获取课程数据
onMounted(() => {
  getCourses()
})

// 计算当前页面显示的课程数据
const paginatedCourses = computed(() => {
  let filteredCourses = courses.value

  if (hideConflicts.value) {
    filteredCourses = filteredCourses.filter((course) => !isConflict(course))
  }

  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredCourses.slice(start, end)
})

// 判断课程是否有冲突
const isConflict = (course: Course) => {
  return false // 默认不做冲突判断
}

// 切换分页
const handlePageChange = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 搜索框部分 */
.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.search-input {
  width: 360px;
}

.search-select {
  width: 150px;
}

.conflict-checkbox {
  margin-left: 10px;
  line-height: 30px;
}

/* 按钮部分 */
.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-start;
  align-items: center;
}

.search-btn,
.clear-btn {
  padding: 10px 20px;
  font-size: 14px;
}

.clear-btn {
  background-color: #f56c6c;
  color: white;
}

.search-btn {
  background-color: #409eff;
  color: white;
}

/* 表格部分 */
.course-table {
  margin-top: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.el-table-column {
  text-align: center;
}

.el-table .el-button {
  transition: transform 0.2s ease;
}

.el-button:hover {
  transform: translateY(-2px);
}

.el-button:active {
  transform: translateY(2px);
}

/* 分页样式 */
.pagination-container {
  margin-top: 20px;
  text-align: center;
}
</style>
