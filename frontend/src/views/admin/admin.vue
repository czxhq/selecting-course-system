<template>
  <div class="admin-container">
    <!-- 侧边导航栏 -->
    <el-aside width="250px" class="admin-aside">
      <div class="sidebar-header">
        <h2 class="system-title">选课管理系统</h2>
      </div>
      <el-menu
        :default-active="activeTab"
        @select="handleSelect"
        class="admin-menu"
        background-color="#f4f4f4"
        text-color="#333"
        active-text-color="#409EFF"
      >
        <el-menu-item index="student" icon="el-icon-user">
          学生管理
        </el-menu-item>
        <el-menu-item index="teacher" icon="el-icon-s-cherry">
          教师管理
        </el-menu-item>
        <el-menu-item index="notification" icon="el-icon-bell">
          通知管理
        </el-menu-item>
        <el-menu-item index="major" icon="el-icon-bell">
          专业管理
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主体内容区 -->
    <el-main class="admin-main">
      <!-- 根据不同选项渲染不同页面 -->
      <student-management v-if="activeTab === 'student'" />
      <teacher-management v-if="activeTab === 'teacher'" />
      <notification-management v-if="activeTab === 'notification'" />
      <MajorManagement v-if="activeTab === 'major'" />
    </el-main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StudentManagement from './StudentManagement.vue'
import TeacherManagement from './TeacherManagement.vue'
import NotificationManagement from './NotificationManagement.vue'
import MajorManagement from './MajorManagement.vue'

const activeTab = ref('student') // 默认显示学生管理

// 切换不同页面
const handleSelect = (index) => {
  activeTab.value = index
}
</script>

<style scoped>
/* 整体容器 */
.admin-container {
  display: flex;
  height: 100vh; /* 让容器占满整个屏幕 */
}

/* 侧边导航栏样式 */
.admin-aside {
  background-color: rgb(244, 244, 244);
  color: #fff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 30px 20px; /* 增加顶部和底部的间距 */
  background-color: #00796b;
  text-align: center;
  margin-bottom: 30px; /* 增加菜单和标题的间隔 */
}

.system-title {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

/* 菜单 */
.admin-menu {
  flex-grow: 1;
  border-right: none;
  margin-top: 20px; /* 增加菜单项与标题之间的间距 */
}

.admin-menu .el-menu-item {
  border-radius: 10px;
  margin-bottom: 10px;
}

.admin-menu .el-menu-item:hover {
  background-color: #4caf50; /* 鼠标悬停时背景色 */
  color: #fff; /* 高亮字体 */
}

.admin-menu .el-menu-item.is-active {
  background-color: #00796b; /* 激活时的背景色 */
  color: #fff;
}

/* 主体内容区 */
.admin-main {
  flex: 1;
  padding: 20px;
  background-color: #f9f9f9;
  overflow-y: auto;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05); /* 主体区域的阴影 */
}

/* 响应式布局（适应较小屏幕设备） */
@media (max-width: 768px) {
  .admin-container {
    flex-direction: column;
  }

  .admin-aside {
    width: 100%;
    height: auto;
  }

  .admin-main {
    padding: 10px;
  }
}
</style>
