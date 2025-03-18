import api from "@/api.js";

export const authRepository = {
  login(email, password) {
    return api.post("/auth/login", { email, password });
  },
  register(userData) {
    return api.post("/auth/register", userData);
  },
  logout() {
    return api.post("/auth/logout");
  },
};
