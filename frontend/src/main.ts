import { createApp } from 'vue'
import App from './App.vue'
import 'normalize.css'
import './assets/css/index.less'
import router from './router'
import pinia from './store'
import 'element-plus/dist/index.css'
import registerIcon from './global/register_icons'
// if (import.meta.env.MODE === 'development') {
//   import('./mock/mock') // 只有在开发模式下才引入 mock
// }
createApp(App).use(router).use(pinia).use(registerIcon).mount('#app')
