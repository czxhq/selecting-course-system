<template>
  <div class="course-table">
    <!-- 切换周的按钮 -->
    <div class="toggle" style="font-weight: 700">
      <span class="icon" style="margin-top: 8px" @click="changeWeek(-1)">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-chevron-left"
          viewBox="0 0 16 16"
        >
          <path
            fill-rule="evenodd"
            d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"
          ></path>
        </svg>
      </span>
      <div
        class="titleName"
        style="
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: space-between;
        "
      >
        <span class="title-week" style="font-size: 14px">{{
          '第' + currentWeek + '周'
        }}</span>
        <span
          class="weekDay"
          style="color: rgb(78, 89, 105); font-weight: 400; margin-top: 10px"
          >{{ getDateOfDay(0) + '~' + getDateOfDay(6) }}</span
        >
      </div>
      <span class="icon" style="margin-top: 8px" @click="changeWeek(1)">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-chevron-right"
          viewBox="0 0 16 16"
        >
          <path
            fill-rule="evenodd"
            d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"
          ></path>
        </svg>
      </span>
    </div>

    <table>
      <thead>
        <tr>
          <th></th>
          <th v-for="(day, index) in daysOfWeek" :key="day">
            <div
              style="
                display: flex;
                flex-direction: column;
                justify-content: space-around;
                align-items: center;
              "
            >
              <span>{{ day }}</span>
              <span style="margin-top: 5px">{{ getDateOfDay(index) }}</span>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="session in sessions" :key="session">
          <td style="font-weight: 700">
            <div
              style="
                display: flex;
                flex-direction: column;
                justify-content: space-around;
                align-items: center;
              "
            >
              <div>{{ session }}节</div>
              <span style="margin-top: 5px">{{
                sessionTimes[session - 1]
              }}</span>
            </div>
          </td>
          <!-- 合并多个 v-for -->
          <td v-for="(day, dayIndex) in daysOfWeek" :key="day" class="cell">
            <div
              v-for="course in coursesOnDay(day, session, dayIndex)"
              :key="course?.courseId"
              class="course"
              :style="getCellStyle(course, session, dayIndex)"
            >
              <div :style="{ color: getFontColor(course) }" class="course-name">
                {{ course?.courseName }}
              </div>
              <div :style="{ color: getFontColor(course) }" class="teacher">
                {{ course?.teacher }}
              </div>
              <div :style="{ color: getFontColor(course) }" class="location">
                {{ course?.location }}
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, onMounted } from 'vue'
import type { PropType } from 'vue'
type Course = {
  courseId: string
  courseName: string
  teacher?: string
  location: string
  time: string[]
}

interface Course1 extends Course {
  index: number
}

const props = defineProps({
  courses: {
    type: Array as PropType<Course[]>,
    required: true
  }
})

const sessionTimes = [
  '8:00~8:45',
  '8:50~9:35',
  '9:50~10:35',
  '10:40~11:25',
  '11:30~12:15',
  '14:00~14:45',
  '14:50~15:35',
  '15:50~16:35',
  '16:40~17:25',
  '17:30~18:15',
  '19:00~19:45',
  '19:50~20:35',
  '20:40~21:25',
  '21:30~22:15'
]
const daysOfWeek = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const sessions = Array.from({ length: 14 }, (_, index) => index + 1) // 1-14节

const startDate = new Date(2025, 1, 24) // 2025年2月24日是第1周的周一
let currentWeek = ref(1)

// 定义四种颜色
const colors = ['#FF6347', '#4682B4', '#FFD700', '#8A2BE2'] // 红色, 蓝色, 黄色, 紫色
const courseList: Course1[] = []
const distributeColor = () => {
  let curIndex = 0
  courseList.length = 0
  for (const course of props.courses) {
    courseList.push(
      Object.assign({}, course, { index: curIndex++ % colors.length })
    )
  }
}

// 根据当前周，计算每个星期的日期
const getDateOfDay = (dayIndex: number) => {
  const date = new Date(startDate)
  date.setDate(date.getDate() + (currentWeek.value - 1) * 7 + dayIndex)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 切换周数
const changeWeek = (delta: number) => {
  const newWeek = currentWeek.value + delta

  // 限制周次范围在 1 到 16 之间
  if (newWeek < 1) {
    currentWeek.value = 1 // 如果小于1，设置为第1周
  } else if (newWeek > 16) {
    currentWeek.value = 16 // 如果大于16，设置为第16周
  } else {
    currentWeek.value = newWeek
  }

  updateSchedule() // 更新课程表
}

// 解析课程时间数据并转化为可用的数据结构
const courseSchedule = ref<Array<Array<Course1 | null>>>(
  Array.from({ length: 14 }, () => Array(7).fill(null))
)

// 函数：根据课程的时间信息，更新课程表
const updateSchedule = () => {
  distributeColor()
  const emptySchedule = Array.from({ length: 14 }, () => Array(7).fill(null))
  const newSchedule: Array<Array<Course1 | null>> = emptySchedule

  courseList.forEach((course) => {
    course.time.forEach((timeRange: string) => {
      const [week, sessionRange, weekRange] = timeRange.split(' ')
      const [startSession, endSession] = sessionRange.split('-').map(Number)
      const [startWeek, endWeek] = weekRange.split('-').map(Number)

      // 解析“周几” (1-7对应周一到周日)
      const days = week.split(',').map(Number)

      // 确保课程在当前周显示
      if (currentWeek.value >= startWeek && currentWeek.value <= endWeek) {
        days.forEach((day) => {
          for (let session = startSession; session <= endSession; session++) {
            newSchedule[session - 1][day - 1] = course
          }
        })
      }
    })
  })

  courseSchedule.value = newSchedule
}

// 计算在某天某节课的所有课程
const coursesOnDay = (
  day: string,
  session: number,
  dayIndex: number
): (Course1 | null)[] => {
  const dayCourses = courseSchedule.value[session - 1][dayIndex]
  return dayCourses ? [dayCourses] : []
}

// 获取课程的颜色（轮流赋予颜色）
const getCourseColor = (course: Course1): string => {
  const index = course.index // 通过课程ID的哈希值获取颜色索引
  return colors[index]
}

// 获取背景颜色的亮度
const getBrightness = (color: string): number => {
  const rgb = color.match(/\w\w/g)!.map((hex) => parseInt(hex, 16)) // 转换为 RGB
  return (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000 // 计算亮度
}

// 获取需要合并的单元格样式
const getCellStyle = (
  course: Course1 | null,
  session: number,
  dayIndex: number
) => {
  if (!course) return {}
  const courseData = courseSchedule.value[session - 1][dayIndex]

  // 合并连续节次的课程单元格
  let rowspan = 1
  for (let i = session; i < 14; i++) {
    if (courseSchedule.value[i][dayIndex]?.courseId === courseData?.courseId) {
      rowspan++
    } else {
      break
    }
  }

  // 获取背景颜色
  const backgroundColor = getCourseColor(course)

  // 判断背景颜色的亮度并设置字体颜色
  const brightness = getBrightness(backgroundColor)
  const textColor = brightness > 150 ? 'black' : 'white'

  return {
    rowspan,
    backgroundColor,
    color: textColor // 设置字体颜色
  }
}

// 获取课程字体颜色，动态调整文本颜色
const getFontColor = (course: Course1 | null) => {
  if (!course) return 'black'

  // 获取背景颜色
  const backgroundColor = getCourseColor(course)

  // 判断背景颜色的亮度并设置字体颜色
  const brightness = getBrightness(backgroundColor)
  return brightness > 150 ? 'black' : 'white' // 若背景亮则字体设为黑色，否则为白色
}

// 监听课程信息变化，更新课程表
watch(() => props.courses, updateSchedule, { immediate: true })
</script>

<style scoped>
.icon {
  cursor: pointer;
}

.icon:hover {
  box-shadow:
    1px 1px 1px rgba(0, 0, 0, 0.2),
    -1px -1px 1px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}

.course-table {
  width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
  color: rgb(5, 103, 179);
  display: flex;
  flex-direction: column;
  align-items: center;
}

table {
  width: 100%;
}

th,
td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ccc;
}

td {
  min-width: 100px;
}

.course {
  padding: 5px;
  background-color: #f5f5f5;
  margin: 2px 0;
  border-radius: 4px;
}

.course-name {
  font-weight: bold;
}

.teacher,
.location {
  font-size: 12px;
  color: #555;
}

.week-navigation {
  margin-bottom: 10px;
}

.week-navigation button {
  margin-right: 10px;
}

.week-navigation span {
  font-weight: bold;
}

.toggle {
  display: flex;
  margin-bottom: 10px;
}
</style>
