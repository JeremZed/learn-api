<script setup>
import store from "@/stores/index.js";
import { MODES } from "@/constants.js";

const changeMode = (event) => {
  store.switcher.setMode(event.target.value);
};
</script>

<template>
  <div class="form-group">
    <label for="mode-select">{{ $t('select_mode') }}</label>
    <select id="mode-select" @change="changeMode" :value="store.switcher.mode">
      <option :value=MODES.LIGHT>{{ $t('mode_light') }}</option>
      <option :value=MODES.DARK>{{ $t('mode_dark') }}</option>
    </select>
  </div>
</template>

<style scoped>

</style>
