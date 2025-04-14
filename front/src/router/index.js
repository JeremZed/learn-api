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
import Account from '../views/pages/dashboard/Account.vue';
import Security from '../views/pages/dashboard/account/Security.vue';
import Information from '../views/pages/dashboard/account/Information.vue';
import Invoice from '../views/pages/dashboard/account/Invoice.vue';


const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
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
    meta: {
      auth: true,
      is_admin: true,
      breadcrumb : 'administration'
    }
  },
  { path: "/account",
    name : 'account',
    component: Account,
    meta: {
      auth: true,
      breadcrumb : 'breadcrumb_account'
    },
  },
  // {
  //   path: '/account/:id',
  //   name: 'accountDetails',
  //   component: AccountDetails,
  //   meta: {
  //     breadcrumb: (route) => `Compte #${route.params.id}`,
  //     parent: 'account'
  //   }
  // },
  { path: "/account/security",
    name : 'security',
    component: Security,
    meta: {
      auth: true,
      breadcrumb : 'breadcrumb_security',
      parent : 'account'
    }
  },
  { path: "/account/information",
    name : 'information',
    component: Information,
    meta: {
      auth: true,
      parent : 'account',
      breadcrumb : 'breadcrumb_information'
    }
  },
  { path: "/account/invoices",
    name : 'invoices',
    component: Invoice,
    meta: {
      auth: true,
      parent : 'account',
      breadcrumb : 'breadcrumb_invoices'
    }
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