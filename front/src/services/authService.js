import { authRepository } from "@/repositories/authRepository.js";

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
};