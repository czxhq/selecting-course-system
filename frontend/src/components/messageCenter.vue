<template>
  <div class="message-center-container">
    <h2>消息中心</h2>

    <div v-if="messages.length > 0" class="messages-list">
      <div
        v-for="(message, index) in paginatedMessages"
        :key="index"
        class="message-item"
      >
        <div class="message-header">
          <h3>{{ message.title }}</h3>
          <span class="message-date">{{ message.date }}</span>
        </div>
        <p>{{ message.content }}</p>
        <div class="message-footer">
          <span>来自: {{ message.from }}</span>
        </div>
      </div>

      <!-- 分页 -->
      <el-pagination
        :current-page="currentPage"
        :page-size="3"
        :total="messages.length"
        @current-change="handlePageChange"
        layout="prev, pager, next"
      />
    </div>
    <div v-else class="no-messages">暂无消息</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useMainPageStore } from '@/store/mainPage'
import axiosrequest from '@/services'
import type { AxiosRequestHeaders } from 'axios'
const props = defineProps<{
  url: string
  id: string
}>()

const store = useMainPageStore()
const messages = ref<Array<any>>([])
const currentPage = ref(1) // 当前页

const pageSize = 3 // 每页显示3条消息

// 请求获取消息
const fetchMessages = async () => {
  const userId = props.id
  axiosrequest
    .post({
      url: props.url,
      data: {
        id: userId
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    .then((response) => {
      if (response.data?.data?.messages) {
        messages.value = response.data.data.messages
      } else {
        ElMessage.warning('没有获取到消息')
      }
    })
    .catch((error) => {
      ElMessage.error('获取消息失败')
    })
}

// 处理分页
const handlePageChange = (page: number) => {
  currentPage.value = page
}

// 分页后的消息
const paginatedMessages = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return messages.value.slice(start, end)
})

onMounted(() => {
  fetchMessages()
})
</script>

<style scoped>
.message-center-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

.messages-list {
  padding: 10px;
}

.message-item {
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  background-color: #fafafa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.message-header h3 {
  font-size: 18px;
  color: #409eff;
  margin: 0;
}

.message-date {
  font-size: 14px;
  color: #999;
}

.message-footer {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.no-messages {
  text-align: center;
  font-size: 18px;
  color: #999;
}

.el-pagination {
  margin-top: 20px;
  text-align: center;
}
</style>
