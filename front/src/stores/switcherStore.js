import { reactive } from "vue";
import { LAYOUTS } from "@/constants.js";

export const switcherStore = reactive({

  theme: localStorage.getItem("theme") || "default",
  mode: localStorage.getItem("mode") || "light",
  layout : localStorage.getItem("layout") || LAYOUTS.DashboardLayout,

  setTheme(newTheme) {
    this.theme = newTheme;
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  },

  setMode(newMode) {
    this.mode = newMode;
    document.documentElement.setAttribute("data-mode", newMode);
    localStorage.setItem("mode", newMode);
  },

  setLayout(newLayout) {
    this.layout = newLayout;
    localStorage.setItem("layout", newLayout);
  },

});


document.documentElement.setAttribute("data-theme", switcherStore.theme);
document.documentElement.setAttribute("data-mode", switcherStore.mode);