import { defineStore } from 'pinia'

export const useTeacherStore = defineStore('teacher', {
  state: () => ({
    teacherId: '' as string
  }),
  actions: {
    setTeacherId(id: string) {
      this.teacherId = id
      localStorage.setItem('id', id)
    },

    clearTeacherId() {
      this.teacherId = ''
      localStorage.setItem('id', '')
    }
  }
})
