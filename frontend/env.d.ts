/// <reference types="vite/client" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent
  export default component
}

declare module 'vue-cal' {
  import { DefineComponent } from 'vue'

  const VueCal: DefineComponent<any, any, any>
  export default VueCal
}

// 定义每个导航项的类型
interface NavItem {
  name: string
  to: string
}

interface Message {
  title: string
  date: string
  content: string
  from: string
}

interface Course {
  courseName: string
  teacher: string
  location: string
  time: string // 时间格式: "1 1-2 1-3"
}
