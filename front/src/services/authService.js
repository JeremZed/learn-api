import { authRepository } from "@/repositories/authRepository.js";
import store from "@/stores/index.js";
import { LAYOUTS } from "@/constants.js";

export const authService = {
  async login(email, password) {
    try {
      const response = await authRepository.login(email, password);
      return response.data;
    } catch (error) {
      throw error.response?.data || "Connexion échouée.";
    }
  },
  async register(userData) {
    try {
      const response = await authRepository.register(userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || "Inscription échouée.";
    }
  },
  async fetchCurrentUser() {
    try {
      const response = await authRepository.getCurrentUser();
      store.user.setUser(response.data.data.user);
      store.switcher.setLayout(LAYOUTS.DASHBOARD);
      return response.data;
    } catch (error) {
      store.user.logout();
      throw "Impossible de récupérer l'utilisateur.";
    }
  }
};