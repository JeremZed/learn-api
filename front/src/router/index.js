import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/authService.js'
import store from "@/stores/index.js";


import Home from '../views/pages/common/Home.vue'
import About from '../views/pages/common/About.vue'
import Login from "../views/pages/common/Login.vue";
import Register from "../views/pages/common/Register.vue";
import PasswordForget from "../views/pages/common/ForgetPassword.vue";
import resetPassword from "../views/pages/common/ResetPassword.vue";

import Admin from "../views/admin/Admin.vue"
import Profil from '../views/pages/dashboard/Profil.vue';


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { auth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  { path: "/login",
    name : 'login',
    component: Login
  },
  { path: "/register",
    name : 'register',
    component: Register
  },
  { path: "/forget-password",
    name : 'forget-password',
    component: PasswordForget
  },
  { path: "/reset-password",
    name : 'reset-password',
    component: resetPassword
  },
  { path: "/admin",
    name : 'admin',
    component: Admin,
    meta: { auth: true, is_admin: true }
  },
  { path: "/profil",
    name : 'profil',
    component: Profil,
    meta: { auth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {

  if(store.user.loading){
    return next();
  }

  if (to.meta.is_admin && !store.user.isAdmin()) {
    next("/");
  }

  next();
});

export default router