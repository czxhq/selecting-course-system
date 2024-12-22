import { defineStore } from 'pinia'

export const useMainPageStore = defineStore('app', {
  state: () => ({
    studentId: '' as string,
    messages: [] as Message[],
    courses: [] as Course[],
    currentPage: 1 as number
  }),
  actions: {
    setStudentId(id: string) {
      this.studentId = id
      localStorage.setItem('id', id)
    },
    clearStudentId() {
      this.studentId = ''
      localStorage.setItem('id', '')
    },
    setMessages(messages: Message[]) {
      this.messages = messages
    },
    setCourses(courses: Course[]) {
      this.courses = courses
    },
    setCurrentPage(page: number) {
      this.currentPage = page
    }
  }
})
