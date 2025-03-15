<script setup>
import { store } from "@/store.js";

const changeTheme = (event) => {
  store.setTheme(event.target.value);
};
</script>

<template>
  <div class="theme-switcher">
    <label for="theme-select">Choisir un thème :</label>
    <select id="theme-select" @change="changeTheme" :value="store.theme">
      <option value="light">Clair</option>
      <option value="dark">Sombre</option>
      <option value="yellow">Jaune</option>
    </select>
  </div>
</template>

<style scoped>
.theme-switcher {
  margin: 10px;
}
</style>
