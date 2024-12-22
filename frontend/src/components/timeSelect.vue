<template>
  <div class="calendar-course">
    <!-- 日历部分 -->
    <div class="calendar">
      <div class="calendar-header">
        <span @click="prevMonth" class="button">«</span>
        <span>{{ currentMonthLabel }}</span>
        <span @click="nextMonth" class="button">»</span>
      </div>
      <div class="calendar-grid">
        <div
          v-for="(day, index) in daysInMonth"
          :key="index"
          :class="[
            'calendar-day',
            {
              selected: selectedDate.getTime() === day.fullDate.getTime(),
              hasCourse: hasCoursesOnDay(day)
            }
          ]"
          @click="selectDate(day)"
        >
          <div class="date-number">{{ day.date }}</div>
          <div v-if="hasCoursesOnDay(day)" class="course-indicator"></div>
        </div>
      </div>
    </div>

    <div style="display: flex; align-items: center; height: 20px">
      <div class="course-indicator1"></div>
      <div>代表当天有课</div>
    </div>
    <!-- 课程列表部分 -->
    <div class="course-list">
      <ul>
        <li v-for="course in coursesOnSelectedDate" :key="course.courseId">
          <div class="course-details">
            <div class="icon" style="background-color: rgba(150, 50, 200, 0.1)">
              <div class="text" style="color: rgb(150, 50, 200)">课</div>
            </div>
            <div class="course-name" style="margin-left: 15px">
              {{ course.courseName }}
            </div>
            <div class="course-location" style="margin-left: 15px">
              {{ course.location }}
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, computed, watch } from 'vue'

type PropType<T> = import('vue').PropType<T> // 类型导入

interface Course {
  courseId: string
  courseName: string
  teacher?: string
  location: string
  time: string[] // ["1 1-2 1-3", "2 1-2 1-3"]
}

const props = defineProps({
  courses: {
    type: Array as PropType<Course[]>,
    required: true
  }
})

// 当前日期
const currentDate = new Date()
const currentMonth = ref(currentDate.getMonth())
const currentYear = ref(currentDate.getFullYear())
const selectedDate = ref(
  new Date(currentYear.value, currentMonth.value, currentDate.getDate())
)

const getDaysInMonth = (year: number, month: number) => {
  const date = new Date(year, month, 1)
  const days = []
  while (date.getMonth() === month) {
    days.push({
      date: date.getDate(),
      fullDate: new Date(date)
    })
    date.setDate(date.getDate() + 1)
  }
  return days
}

const daysInMonth = computed(() =>
  getDaysInMonth(currentYear.value, currentMonth.value)
)
const currentMonthLabel = computed(() => {
  const months = [
    '1月',
    '2月',
    '3月',
    '4月',
    '5月',
    '6月',
    '7月',
    '8月',
    '9月',
    '10月',
    '11月',
    '12月'
  ]
  return `${months[currentMonth.value]} ${currentYear.value}`
})

// 选择日期后的课程
const selectedDateLabel = computed(() => {
  const date = selectedDate.value
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
})

// 获取某天有课的课程
const coursesOnSelectedDate = computed(() => {
  return props.courses.filter((course: Course) => {
    return course.time.some((timeSlot: string) => {
      return isDateInCourseTime(timeSlot, selectedDate.value)
    })
  })
})

// 判断日期是否在课程时间内
const isDateInCourseTime = (timeSlot: string, date: Date) => {
  const dayOfWeek = date.getDay() // 获取选中的日期是周几 (0=星期日, 1=星期一, ...)

  // 解析课程时间
  const timeParts = timeSlot.split(' ') // 例如 "1 1-2 1-3"
  const weekDay = parseInt(timeParts[0]) % 7 // 将课程的星期几转换为从0开始（星期一是1, 但getDay()返回0=星期日）

  const weekRange = timeParts[2].split('-') // 获取周次范围
  const startWeek = parseInt(weekRange[0]) // 第几周
  const endWeek = parseInt(weekRange[1]) // 到第几周

  // 检查课程是否在该周
  const currentWeek = getWeekOfYear(date) // 获取当前周次
  if (currentWeek < startWeek || currentWeek > endWeek) {
    return false
  }

  // 检查是否为同一周的星期几
  return dayOfWeek === weekDay
}

// 获取当前周数（假设学期从2月24日的第一周开始）
const getWeekOfYear = (date: Date) => {
  const startOfYear = new Date(date.getFullYear(), 1, 24) // 假设学期从2025年2月24日（周一）开始
  const diff = date.getTime() - startOfYear.getTime()
  const oneDay = 1000 * 60 * 60 * 24
  const dayOfYear = Math.floor(diff / oneDay)
  return Math.floor(dayOfYear / 7) + 1 // 计算当前是第几周
}

// 根据选择的日期更新课程显示
const selectDate = (day: { date: number; fullDate: Date }) => {
  selectedDate.value = day.fullDate
}

// 是否某天有课
const hasCoursesOnDay = (day: { date: number; fullDate: Date }) => {
  return props.courses.some((course: Course) => {
    return course.time.some((timeSlot: string) => {
      return isDateInCourseTime(timeSlot, day.fullDate)
    })
  })
}

// 切换到上个月
const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

// 切换到下个月
const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

// watch更新
watch([currentMonth, currentYear], () => {
  selectedDate.value = new Date(
    currentYear.value,
    currentMonth.value,
    selectedDate.value.getDate()
  )
})
</script>

<style scoped>
.icon {
  border-radius: 0 12px 12px 12px;
  width: 38px;
  height: 38px;
  min-width: 38px;
  max-height: 38px;
  background: rgba(150, 97, 188, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-course {
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y: auto;
  overflow-x: auto;
}

.calendar {
  margin-bottom: 20px;
  min-height: 160px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.calendar-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
}

.calendar-day.selected {
  background-color: #3f51b5;
  color: white;
}

.calendar-day.hasCourse {
  background-color: #e1bee7;
}

.course-indicator {
  background-color: purple;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 5px;
}

.course-indicator1 {
  background-color: purple;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.course-list {
  margin-top: 20px;
}

.course-name {
  font-weight: bold;
}

.course-details {
  font-size: 14px;
  color: gray;
  display: flex;
  align-items: center;
  min-height: 60px;
  border: 1px solid rgba(200, 200, 200, 0.6);
  border-radius: 4px;
  padding-left: 10px;
}

.button {
  cursor: pointer;
}
</style>
