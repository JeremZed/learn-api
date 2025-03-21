import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { i18n, loadLocaleMessages } from "./locales";
import { createHead } from "@vueuse/head";

import "./assets/css/common.scss";
import "./assets/css/responsive.scss";
import "./assets/css/mode_dark.scss";
import "./assets/css/mode_light.scss";

import "./assets/css/theme_default.scss";
import "./assets/css/theme_pink.scss";

// import "./assets/css/theme_yellow.css";

const head = createHead();

const app = createApp(App)
app.use(router);
app.use(i18n);
app.use(head);
app.mount('#app');

loadLocaleMessages(i18n.global.locale.value);