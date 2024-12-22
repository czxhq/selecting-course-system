<template>
  <div class="container">
    <div class="intro-section">
      <div class="intro-left">
        <div class="intro-text">
          <h2 class="intro1">专业选课，轻松管理</h2>
          <h3 class="intro2">助力学业高效</h3>
        </div>
        <button class="start-button" @click="handleStartButtonClick">
          开始!
        </button>
      </div>
      <div class="intro-right">
        <img src="../../assets/img/home-1-662x662.webp" alt="" />
      </div>
    </div>
    <div class="login-section">
      <div ref="loginTitle" class="login-title"><div>登录入口</div></div>
      <div class="login-cards">
        <el-card
          class="login-card"
          :body-style="{ padding: '20px' }"
          @click="goToLogin('teacher')"
        >
          <div class="st-img">
            <img
              src="/src/assets/img/school-svgrepo-com.svg"
              alt=""
              width="100px"
              height="100px"
            />
          </div>
          <div class="login-card-title">教师登录</div>
          <el-button class="login-card-button">进入</el-button>
        </el-card>
        <el-card
          class="login-card"
          :body-style="{ padding: '20px' }"
          @click="goToLogin('student')"
        >
          <div class="st-img">
            <img
              src="/src/assets/img/student-svgrepo-com.svg"
              alt=""
              width="100px"
              height="100px"
            />
          </div>
          <div class="login-card-title">学生登录</div>
          <el-button class="login-card-button">进入</el-button>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const loginTitle = ref<HTMLElement | null>(null) // 用来引用 "登录入口" 的 div 元素

// 跳转到登录页面
const goToLogin = (role: string) => {
  if (role === 'teacher') {
    router.push('/teacher-login') // 假设教师登录的路由是 '/teacher-login'
  } else if (role === 'student') {
    router.push('/student-login') // 假设学生登录的路由是 '/student-login'
  }
}

// 按钮点击事件处理
const handleStartButtonClick = () => {
  const token = localStorage.getItem('token')

  if (token) {
    // 如果 token 存在，跳转到主页
    if (token === 'stu') {
      router.push('/main') // 假设跳转到用户首页
    } else if (token === 'tea') {
      router.push('/teacher-page')
    } else if (token === 'adm') {
      router.push('/admin')
    }
  } else {
    // 如果 token 不存在，滚动到登录入口位置
    if (loginTitle.value) {
      loginTitle.value.scrollIntoView({ behavior: 'smooth' }) // 平滑滚动到 "登录入口" 位置
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
}

.intro-section {
  box-sizing: border-box;
  height: 790px;
  width: 100vw;
  background: linear-gradient(to right, #145a9f, #2c77c1, #145a9f);
  padding-top: 75px;
  display: flex;
  color: white;
}

.intro-left {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-left: 15vw;
}

.intro-right {
  width: 50%;
  height: 100%;
}

.start-button {
  width: 144px;
  height: 51.6px;
  border-radius: 22px;
  border: 0;
  background-color: rgb(239, 158, 8);
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    background-color 0.3s ease; /* 添加平滑过渡 */
}

/* 悬停时动画 */
.start-button:hover {
  background-color: rgb(255, 145, 0); /* 背景色变化 */
  transform: scale(1.1); /* 增大按钮 */
}

/* 点击时动画 */
.start-button:active {
  transform: scale(0.95); /* 点击时按钮缩小 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加点击时的阴影效果 */
}

/* 加载动画效果 */
.start-button {
  animation: buttonFadeIn 1s ease-out;
}

.login-section {
  background-color: rgb(249, 248, 248);
  height: 700px;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.login-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 30px;
  color: #333;
  animation: fadeInUp 1s ease-out;
  background-color: white;
  border-radius: 10px;
  height: 70px;
  width: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-cards {
  display: flex;
  gap: 100px;
}

.login-card {
  width: 400px;
  height: 350px;
  border-radius: 12px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  cursor: pointer;
  padding-top: 50px;
}

.login-card:hover {
  transform: translateY(-10px);
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
}

.login-card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 40px;
  text-align: center;
  padding-top: 50px;
}

.login-card-button {
  width: 100%;
  background-color: #409eff;
  color: white;
  font-weight: 600;
}

.st-img {
  text-align: center;
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes buttonFadeIn {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.intro-text {
  box-sizing: border-box;
  flex: 0 0 60%;
  padding-top: 180px;
  display: flex;
  flex-direction: column;
}

.intro1 {
  font-size: 48px;
  font-weight: 800;
}

.intro2 {
  padding-top: 20px;
  font-size: 48px;
  font-weight: 100;
}

.intro3 {
  font-weight: 300;
  font-size: 22px;
  padding-top: 50px;
}

@media (max-width: 768px) {
  .container {
    margin-top: 0;
  }

  .intro-section {
    padding-top: 0;
    flex-direction: column;
  }

  .intro-right {
    display: none;
  }

  .login-section {
    margin-top: 150px;
  }

  .login-cards {
    display: flex;
    flex-direction: column;
  }
}
</style>
