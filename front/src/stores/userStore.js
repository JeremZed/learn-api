import { reactive } from "vue";
import { authService } from "@/services/authService.js";

export const userStore = reactive({
  user: null,
  token: localStorage.getItem("token") || null,
  isAuthenticated: !!localStorage.getItem("token"),

  setUser(userData, token) {
    this.isAuthenticated = true;
    this.user = userData;
    this.token = token;
    localStorage.setItem("token", token);
  },

  logout() {
    this.isAuthenticated = false;
    this.user = null;
    this.token = null;
    localStorage.removeItem("token");
  },

  isAdmin(){
    return this.user && this.user.role === "admin";
  },

  async init() {
    if (this.token) {
      try {
        await authService.fetchCurrentUser();
      } catch (error) {
        console.error("Erreur lors de la récupération de l'utilisateur :", error);
      }
    }
  }
});
