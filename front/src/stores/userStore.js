import { reactive } from "vue";
import { authService } from "@/services/authService.js";

export const userStore = reactive({
  user: null,
  isAuthenticated: false,
  loading: true,

  setUser(userData) {
    this.isAuthenticated = true;
    this.user = userData;
    this.loading = false;
  },

  logout() {
    this.isAuthenticated = false;
    this.user = null;
    this.loading = true;
  },

  isAdmin(){
    return this.user && this.user.role === "admin";
  },

  async init() {
    try {
        const response = await authService.fetchCurrentUser();
        if (response?.data?.user) {
          this.setUser(response.data.user);
        }

    } catch (error) {
      throw new Error("Erreur lors de la récupération de l'utilisateur :", error);
    }
  }
});
