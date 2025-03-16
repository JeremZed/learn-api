import { reactive } from "vue";

export const userStore = reactive({
  user: null,
  token: localStorage.getItem("token") || null,


  setUser(userData, token) {
    this.user = userData;
    this.token = token;
    localStorage.setItem("token", token);
  },

  logout() {
    this.user = null;
    this.token = null;
    localStorage.removeItem("token");
  },
});

