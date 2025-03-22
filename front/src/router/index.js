import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/authService.js'


import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Login from "../views/Login.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { auth : true }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: { auth: true }
  },
  { path: "/login",
    name : 'login',
    component: Login
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.auth && !authService.isAuthenticated()) {
    next("/login");
  } else {
    next();
  }
});

export default router