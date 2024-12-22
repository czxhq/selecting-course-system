import { defineStore } from 'pinia'

export const useToken = defineStore('token', {
  state: () => ({
    token: localStorage.getItem('token') || ''
  }),
  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    clearToken() {
      this.token = ''
      localStorage.removeItem('token')
    }
  }
})
