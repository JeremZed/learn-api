import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/authService.js'
import store from "@/stores/index.js";


import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Login from "../views/Login.vue";

import Admin from "../views/admin/Admin.vue"

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
  { path: "/admin",
    name : 'admin',
    component: Admin,
    meta: { auth: true, is_admin: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.auth && !authService.isAuthenticated()) {
    next("/login");
  }
  else if (to.meta.is_admin && !store.user.isAdmin()) {
    next("/");
  }
  else {
    next();
  }
});

export default router