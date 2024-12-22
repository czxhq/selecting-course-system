<template>
  <TimeSelect :courses="courses" style="margin-top: 100px"></TimeSelect>
</template>
<script lang="ts" setup>
import axiosrequest from '@/services'
import type { AxiosRequestHeaders } from 'axios'
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

const courses = ref<any[]>([])
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
  } catch (error) {
    ElMessage.error('获取课程信息失败:')
  }
}
onMounted(async () => {
  await fetchCourses()
  console.log(courses.value)
})
</script>
<style scoped></style>
