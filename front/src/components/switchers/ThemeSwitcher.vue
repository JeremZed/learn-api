<script setup>
import store from "@/stores/index.js";
import { THEMES } from "@/constants.js";

const changeTheme = (event) => {
  store.switcher.setTheme(event.target.value);
};
</script>

<template>
  <div class="theme-switcher">
    <label for="theme-select">Choisir un thème :</label>
    <select id="theme-select" @change="changeTheme" :value="store.switcher.theme">
      <option :value=THEMES.DEFAULT>Défaut</option>
      <option :value=THEMES.PINK>Pink</option>
    </select>
  </div>
</template>

<style scoped>

</style>
