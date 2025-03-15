import { reactive } from "vue";

export const store = reactive({
  user: null, // Stocke les infos de l'utilisateur
  token: localStorage.getItem("token") || null,

  theme: localStorage.getItem("theme") || "light",

  setTheme(newTheme) {
    this.theme = newTheme;
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  },

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


document.documentElement.setAttribute("data-theme", store.theme);