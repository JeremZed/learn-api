import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import "./assets/css/common.css";
import "./assets/css/theme_default.css";
import "./assets/css/theme_dark.css";
import "./assets/css/theme_yellow.css";


const app = createApp(App)
app.use(router)
app.mount('#app')