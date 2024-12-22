<template>
  <div ref="chart" style="width: 100%; height: 400px"></div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import * as echarts from 'echarts'
import type { AxiosRequestHeaders } from 'axios'
import axiosrequest from '@/services'
import { ElMessage } from 'element-plus'

type Data = {
  [key: string]: string
}

// 数据格式
const rawData = ref({
  C: '',
  E: '',
  GM: '',
  CM: '',
  CG: '',
  G: ''
})

const fetchRawData = async () => {
  await axiosrequest
    .post({
      url: '/home/creditProgress/',
      data: {
        studentId: localStorage.getItem('id')
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    .then((response) => {
      rawData.value = response.data.result
    })
    .catch((error) => {
      ElMessage.error('获取学分信息失败')
    })
}

// 使用 ref 获取 DOM 元素
const chart = ref<HTMLDivElement | null>(null)

// 挂载后初始化 ECharts
onMounted(async () => {
  await fetchRawData()
  if (chart.value) {
    const myChart = echarts.init(chart.value)

    // 数据处理
    const categories = Object.keys(rawData.value).map((item) => {
      if (item === 'C') {
        return '必修'
      } else if (item === 'E') {
        return '选修'
      } else if (item === 'GM') {
        return '一般专业'
      } else if (item === 'CM') {
        return '核心专业'
      } else if (item === 'CG') {
        return '核心通识'
      } else if (item == 'G') {
        return '一般通识'
      }
      return ''
    })
    const data: Data = rawData.value
    const completedValues = Object.keys(data).map((key) => {
      const [completed, total] = String(data[key]).split('/').map(Number)
      return completed
    })
    const totalValues = Object.keys(data).map((key) => {
      const [completed, total] = String(data[key]).split('/').map(Number)
      return total
    })

    // ECharts 配置项
    const option = {
      title: {
        text: '个人进度',
        left: 'center'
      },
      tooltip: {},
      xAxis: {
        type: 'category',
        data: categories
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '已选',
          type: 'bar',
          data: completedValues,
          barWidth: '40%',
          itemStyle: {
            color: '#4CAF50'
          }
        },
        {
          name: '总计',
          type: 'bar',
          data: totalValues,
          barWidth: '40%',
          itemStyle: {
            color: '#FF9800'
          }
        }
      ]
    }

    // 设置图表配置项并渲染
    myChart.setOption(option)
  }
})
</script>

<style scoped>
/* 这里可以为组件添加样式 */
</style>
