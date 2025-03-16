<script setup>
import store from "@/stores/index.js";
import { LAYOUTS } from "@/constants.js";

const changeLayout = (event) => {
  store.switcher.setLayout(event.target.value);
};
</script>

<template>
  <div class="layout-switcher">
    <label for="layout-select">Choisir un layout :</label>
    <select id="layout-select" @change="changeLayout" :value="store.switcher.layout">
      <option :value=LAYOUTS.DEFAULT >Default</option>
      <option :value=LAYOUTS.SECOND >Second</option>
    </select>
  </div>
</template>

<style scoped>

</style>
