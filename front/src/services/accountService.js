import { accountRepository } from "@/repositories/accountRepository.js";

export const accountService = {

  async changePassword(userData) {
    try {
      const response = await accountRepository.changePassword(userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || "Modification échouée.";
    }
  },
};