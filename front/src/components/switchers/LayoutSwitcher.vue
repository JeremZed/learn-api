<script setup>
import store from "@/stores/index.js";
import { LAYOUTS } from "@/constants.js";

const changeLayout = (event) => {
  store.switcher.setLayout(event.target.value);
};
</script>

<template>
  <div class="form-group">
    <label for="layout-select">{{ $t('select_layout') }}</label>
    <select id="layout-select" @change="changeLayout" :value="store.switcher.layout">
      <option :value=LAYOUTS.DEFAULT >{{ $t('layout_default') }}</option>
      <option :value=LAYOUTS.SECOND >{{ $t('layout_pink') }}</option>
    </select>
  </div>
</template>

<style scoped>

</style>
