<template>
  <div class="loginContainer">
    <Bgst1 class="bgst1"></Bgst1>
    <LoginPane
      :url="'/admin-login/'"
      :username="'用户名'"
      :to="'/admin/'"
    ></LoginPane>
  </div>
</template>
<script setup lang="ts"></script>
<style scoped>
.loginContainer {
  margin: 0;
  height: 100vh;
  width: 100%;
  color: black;
  background: #0c0c0b;
  overflow: hidden;
  display: grid;
  place-content: center;
}

.bgst1 {
  position: absolute;
  z-index: 0;
}
</style>
