import api from "@/api.js";

export const accountRepository = {

  changePassword(userData) {
    return api.put("/account/password", userData);
  },
};
