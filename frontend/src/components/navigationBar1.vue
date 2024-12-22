<template>
  <button class="collapse-btn" @click="toggleMenu" v-if="isMobile">
    <span :class="{ rotate: !shouldShow }"></span>
  </button>
  <nav
    class="navbar"
    :class="{ scrolled: hasScrolled || isMobile }"
    v-if="shouldShow"
  >
    <div class="navbar-container">
      <!-- 动态SVG Logo -->
      <div class="logo">
        <div>选课管理系统</div>
      </div>
      <ul class="nav-links">
        <li v-for="item in navItems" :key="item.to">
          <router-link
            :to="item.to"
            :class="{ scrolled: hasScrolled || isMobile }"
            >{{ item.name }}</router-link
          >
        </li>
      </ul>
      <div class="github-link">
        <slot></slot>
        <a
          href="https://github.com/czxhq/selecting-course-system"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src="@/assets/img/github-mark-white.svg" alt="GitHub" />
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
const props = defineProps<{
  navItems: NavItem[]
}>()
const shouldShow = ref(true)

// 控制是否为手机模式（小屏幕）
const isMobile = ref(false)

const hasScrolled = ref(false) // 用于判断页面是否滚动

// 检测窗口大小并更新 isMobile 的状态
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

const handleScroll = () => {
  // 判断页面是否滚动到一定位置，决定是否显示原背景色
  hasScrolled.value = window.scrollY > 0
}

// 初始化时检测视口大小
onMounted(() => {
  checkMobile()
  handleScroll()
  window.addEventListener('resize', checkMobile)
  window.addEventListener('scroll', handleScroll)
})
watch(isMobile, (newV) => {
  if (!newV) {
    shouldShow.value = true
  } else {
    shouldShow.value = false
  }
})

const toggleMenu = () => {
  shouldShow.value = !shouldShow.value
}
</script>

<style scoped>
.collapse-btn {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  z-index: 1100;
  opacity: 0.7; /* 半透明效果 */
  transition: opacity 0.3s ease;
}

.collapse-btn span {
  display: block;
  width: 20px;
  height: 20px;
  border: solid 3px #fff;
  border-width: 0 3px 3px 0;
  transform: rotate(135deg);
  transition: transform 0.3s ease;
}

.collapse-btn span.rotate {
  transform: rotate(-45deg);
  border-color: #2c2b2b;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 75px;
  background-color: rgba(0, 0, 0, 0);
  z-index: 1000;
  transition:
    background-color 0.3s,
    box-shadow 0.3s;
}

.navbar.scrolled {
  background-color: #1e1e1e;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.navbar-container {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 0 2vw;
  padding-left: 12.5vw;
}

.logo {
  align-items: center;
  color: #ffffff;
  font-size: 1.5vw;
  font-weight: bold;
  transition: color 0.3s;
  flex: 0 0 15vw;
  padding-left: 2.5vw;
  line-height: 75px;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 4vw;
  flex: 0 0 40vw;
  margin-left: 2vw;
}

.nav-links li {
  position: relative;
}

.nav-links a {
  color: #ffffff;
  text-decoration: none;
  font-size: 1rem;
  padding: 0.5rem 0;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #f09f07;
}

.nav-links a.scrolled:hover {
  color: #6779f5;
}

.nav-links a.scrolled::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -5px;
  height: 2px;
  background-color: #6779f5;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.nav-links a::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -5px;
  height: 2px;
  background-color: #f09f07;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.nav-links a:hover::after {
  transform: scaleX(1);
}

.github-link img {
  width: 28px;
  height: 28px;
  transition: transform 0.3s;
}

.github-link img:hover {
  transform: scale(1.1);
}

.github-link {
  width: 34vw;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

/* 媒体查询：当视口宽度小于768px时，导航栏竖向排列 */
@media (max-width: 768px) {
  .navbar {
    width: 25%;
    height: 100%;
  }

  .navbar-container {
    flex-direction: column; /* 竖向排列 */
    align-items: center;
    padding-left: 0;
  }

  .logo {
    flex: 0 0 20vh;
    width: 100%; /* 让logo宽度充满容器 */
    text-align: center;
    line-height: 20vh;
    padding-left: 0; /* 去掉左侧padding */
    margin-bottom: 1rem; /* 增加logo和导航链接之间的间距 */
    font-size: 2vw;
  }

  .nav-links {
    flex: 0 0 40vh;
    gap: 8vh; /* 增加导航项之间的垂直间距 */
    flex-direction: column; /* 竖向排列导航项 */
    align-items: center;
    margin-left: 0;
  }

  .nav-links li {
    width: 100%; /* 让每个导航项占满容器宽度 */
    text-align: center;
  }

  .github-link {
    flex: 0 0 20vh;
    width: 100%; /* GitHub 链接宽度也改为100% */
    flex-direction: column;
    justify-content: flex-end; /* GitHub 图标居中 */
    text-align: center;
  }

  .github-link img {
    width: 32px;
    height: 32px;
  }
}
</style>
