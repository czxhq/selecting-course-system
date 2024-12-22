<template>
  <NavigationBar1 :nav-items="navItems"></NavigationBar1>
  <router-view></router-view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
const routes: NavItem[] = [
  { name: 'Home', to: '/' },
  { name: 'About', to: '/home/about' },
  { name: 'Help', to: '/home/help' }
]
const navItems = ref(routes)
</script>

<style></style>
