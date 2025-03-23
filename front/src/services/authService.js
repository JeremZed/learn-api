import { authRepository } from "@/repositories/authRepository.js";
import store from "@/stores/index.js";

export const authService = {
  async login(email, password) {
    try {
      const response = await authRepository.login(email, password);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || "Connexion échouée.";
    }
  },
  async register(userData) {
    try {
      const response = await authRepository.register(userData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || "Inscription échouée.";
    }
  },
  async fetchCurrentUser() {
    try {
      const response = await authRepository.getCurrentUser();
      store.user.setUser(response.data.data.user, localStorage.getItem("token"));
      return response.data;
    } catch (error) {
      store.user.logout();
      throw "Impossible de récupérer l'utilisateur.";
    }
  },
  isAuthenticated() {
    return localStorage.getItem("token") !== null;
  },
  async logout(){
    localStorage.removeItem('token')
    return true
  }
};