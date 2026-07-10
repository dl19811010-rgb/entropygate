import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import router from './router'
import App from './App.vue'
import './styles/global.css'
// 【Phase 3】移动端响应式增强
import './styles/responsive.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(naive)

// 【Phase 3】注册图片懒加载指令 v-lazy
import vLazy from './directives/lazy'
app.directive('lazy', vLazy)

app.mount('#app')
