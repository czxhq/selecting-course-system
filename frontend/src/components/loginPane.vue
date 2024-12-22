<template>
  <div class="login">
    <div class="logintext">Login</div>
    <div class="field">
      <input
        type="text"
        v-model="id"
        placeholder=""
        @focus="onFocus"
        @blur="onBlur"
        @input="checkAndClear"
      />
      <div class="placeholder">{{ props.username }}</div>
    </div>
    <div class="field">
      <input
        type="password"
        v-model="password"
        placeholder=""
        @focus="onFocus"
        @blur="onBlur"
        @input="checkAndClear"
      />
      <div class="placeholder">密码</div>
    </div>
    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
    <div class="loginbtn" @click="handleLogin">登录</div>
    <div class="homebtn" @click="goHome">返回首页</div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToken } from '@/store/token'
import axiosrequest from '@/services'
import type { AxiosRequestHeaders } from 'axios'
import { useMainPageStore } from '@/store/mainPage'
import { useTeacherStore } from '@/store/teacher'

const props = defineProps<{
  url: string
  username: string
  to: string
}>()

const id = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()
const store = useToken()
const teacherStore = useTeacherStore()
const mainPageStore = useMainPageStore()
const checkAndClear = () => {
  if (id.value && password.value) {
    errorMessage.value = ''
  }
}
const onFocus = (event: FocusEvent) => {
  const field = (event.target as HTMLInputElement).closest('.field')
  if (field) {
    field.classList.add('focused')
  }
}

const goHome = () => {
  router.push('/home')
}

const onBlur = (event: FocusEvent) => {
  const field = (event.target as HTMLInputElement).closest('.field')
  if (field) {
    if (!(event.target as HTMLInputElement).value) {
      field.classList.remove('focused')
    }
  }
}

const handleLogin = async () => {
  errorMessage.value = '' // 清空错误信息

  // 校验学号和密码不能为空
  if (!id.value || !password.value) {
    errorMessage.value = '学号和密码不能为空'
    return
  }

  axiosrequest
    .post({
      url: props.url,
      data: {
        id: id.value,
        password: password.value
      },
      headers: {
        'Content-Type': 'application/json'
      } as AxiosRequestHeaders
    })
    .then((response) => {
      if (response.data.result === 'success') {
        if (props.url === '/login/') {
          store.setToken('stu')
          mainPageStore.setStudentId(id.value)
        } else if (props.url === '/teacher-login/') {
          store.setToken('tea')
          teacherStore.setTeacherId(id.value)
        } else if (props.url === '/admin-login/') {
          store.setToken('adm')
        }

        router.push(props.to)
      } else {
        errorMessage.value = '登录失败，请检查学号和密码'
      }
    })
    .catch((error) => {
      errorMessage.value = '网络错误，请稍后重试'
    })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.login {
  background: rgba(255, 255, 255, 0); /* 设置透明背景 */
  width: 20rem;
  padding: 1.5rem;
  border-radius: 1.5rem;
  display: grid;
  gap: 0.5rem;
  border: 3px solid white; /* 设置白色边框 */
}

.logintext {
  font-family: 'Inter';
  color: white;
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

@property --anim {
  syntax: '<number>';
  inherits: true;
  initial-value: 0;
}

.field {
  background: white;
  border-radius: 0.75rem;
  position: relative;
  height: 2.5rem;
  --anim: 0;
  transition: --anim 500ms ease;

  background: linear-gradient(
      to right,
      white calc(clamp(0, (var(--anim) - 0.75) / 0.25, 1) * 33%),
      transparent calc(clamp(0, (var(--anim) - 0.75) / 0.25, 1) * 33%),
      transparent calc(100% - clamp(0, (var(--anim) - 0.75) / 0.25, 1) * 33%),
      white calc(100% - clamp(0, (var(--anim) - 0.75) / 0.25, 1) * 33%)
    ),
    linear-gradient(
      to top,
      transparent calc(15% + clamp(0, (var(--anim) - 0.65) / 0.1, 1) * 70%),
      #202122 calc(15% + clamp(0, (var(--anim) - 0.65) / 0.1, 1) * 70%)
    ),
    linear-gradient(
      to right,
      transparent calc(50% - clamp(0, var(--anim) / 0.65, 1) * 50%),
      white calc(50% - clamp(0, var(--anim) / 0.65, 1) * 50%),
      white calc(50% + clamp(0, var(--anim) / 0.65, 1) * 50%),
      transparent calc(50% + clamp(0, var(--anim) / 0.65, 1) * 50%)
    ),
    linear-gradient(#202122, #202122);
}

.field:has(input:focus) {
  --anim: 1;
}

.field > .placeholder {
  pointer-events: none;
  position: absolute;
  inset: 0;
  display: grid;
  place-content: center;
  color: white;
  font-family: 'Inter';
  transition: transform 500ms ease;
}

.field:has(input:focus) > .placeholder,
.field:has(input:not(:placeholder-shown)) > .placeholder {
  transform: translateY(-50%) scale(0.85);
}

.field > input {
  display: flex;
  align-items: center;
  padding-left: 1rem;
  color: white;
  position: absolute;
  inset: 0.125rem;
  border-radius: 0.625rem;
  border: none;
  outline: none;
  background: #202122;
}

.loginbtn {
  margin-top: 0.5rem;
  background: radial-gradient(
    circle at center,
    #6779f5 calc(-50% + var(--anim) * 150%),
    #202122 calc(var(--anim) * 100%)
  );
  border-radius: 0.75rem;
  position: relative;
  height: 2.5rem;
  display: grid;
  place-content: center;
  color: white;
  font-family: 'Inter';
  --anim: 0;
  transition:
    --anim 500ms ease,
    color 500ms ease;
}

.homebtn {
  color: white;
  margin-top: 20px;
  border: 1px solid white;
  border-radius: 5px;
  display: inline-block;
  text-align: center;
  width: 70px;
  height: 30px;
  line-height: 30px;
  background: #202122;
  position: relative;
  overflow: hidden;
}

.homebtn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.5),
    rgba(255, 255, 255, 0)
  );
  transform: scale(0);
  transition: transform 0.4s ease-out;
}

.homebtn:hover {
  cursor: pointer;
}

.homebtn:hover::before {
  transform: scale(5); /* 扩大渐变效果 */
}

.loginbtn:hover {
  --anim: 1;
  color: white;
  cursor: pointer;
}

.error-message {
  text-align: center;
  color: red;
}
</style>
