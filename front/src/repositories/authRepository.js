import api from "@/api.js";

export const authRepository = {
  login(email, password) {
    return api.post("/auth/login", { email, password });
  },
  register(userData) {
    return api.post("/auth/register", userData);
  },
  resetPassword(userData) {
    return api.post("/auth/reset-password", userData);
  },
  queryForgetPassword(email) {
    return api.post("/auth/query-reset-password", {email});
  },
  logout() {
    return api.post("/auth/logout");
  },
  getCurrentUser() {
    return api.get("/auth/me");
  }
};
