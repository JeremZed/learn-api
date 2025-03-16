<script setup>
import store from "@/stores/index.js";
import { MODES } from "@/constants.js";

const changeMode = (event) => {
  store.switcher.setMode(event.target.value);
};
</script>

<template>
  <div class="mode-switcher">
    <label for="mode-select">Choisir un mode :</label>
    <select id="mode-select" @change="changeMode" :value="store.switcher.mode">
      <option :value=MODES.LIGHT>Clair</option>
      <option :value=MODES.DARK>Sombre</option>
    </select>
  </div>
</template>

<style scoped>

</style>
