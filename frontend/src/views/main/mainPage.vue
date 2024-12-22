<template>
  <div class="root">
    <div class="section1">
      <div class="time-container">
        <h3 style="font-size: 18px; font-weight: 700; margin-bottom: 20px">
          我的课表
        </h3>
        <TimeTable :courses="courses" :key="renderkeyTimeTable"></TimeTable>
      </div>
      <div class="right-section">
        <div class="message-section">
          <MessageCenter
            :url="'/home/messages/'"
            :id="studentId"
            style="height: 462px"
          ></MessageCenter>
        </div>
        <div class="time-select">
          <h3 style="font-size: 28px; font-weight: 700">日程安排</h3>
          <TimeSelect :courses="courses" :key="renderkeyTimeTable"></TimeSelect>
        </div>
      </div>
    </div>

    <div class="section2">
      <mainSelection @change="update"></mainSelection>
      <MainAnalyze
        :key="renderkeyTimeTable"
        style="margin-top: 15px"
      ></MainAnalyze>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import TimeTable from '@/components/timeTable.vue'
import mainSelection from './mainSelection.vue'
import { useMainPageStore } from '@/store/mainPage'
import axiosrequest from '@/services'
import type { AxiosRequestHeaders } from 'axios'
import { ElMessage } from 'element-plus'
import MainAnalyze from './mainAnalyze.vue'

const store = useMainPageStore()
const courses = ref<any[]>([])
const renderkeyTimeTable = ref(0)
const studentId: string = localStorage.getItem('id') as string
const fetchCourses = async () => {
  axiosrequest
    .post({
      url: '/home/courses/',
      data: {
        studentId: studentId
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    .then((response) => {
      courses.value = response.data.data.courses
    })
    .catch((error) => {
      console.log(error)
      ElMessage.error('获取课程信息失败')
    })
}

const update = async () => {
  updateRender()
}
const updateRender = () => {
  fetchCourses().then(() => {
    renderkeyTimeTable.value++
  })
}

onMounted(() => {
  fetchCourses()
})
</script>

<style>
* {
  box-sizing: border-box;
}

.root {
  background-color: rgb(240, 245, 255);
  display: flex;
  flex-direction: column;
  width: 100%;
}

.section1 {
  display: flex;
  flex-wrap: wrap;
  padding: 40px 30px;
  margin-left: 15px;
}

.time-container {
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

.section2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 20px;
  background-color: white;
  border-radius: 30px;
  width: 97%;
  align-self: center;
}
</style>
