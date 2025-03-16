
<script setup>

import DefaultLayout from "@/views/layouts/DefaultLayout.vue";
import SecondLayout from "@/views/layouts/SecondLayout.vue";

import { LAYOUTS } from "@/constants.js";

import { computed } from "vue";
import store from "@/stores/index.js";

const layoutComponent = computed(() => {
  let l;

  switch (store.switcher.layout) {
    case LAYOUTS.DEFAULT:
      l = DefaultLayout
      break;
    case LAYOUTS.SECOND:
      l = SecondLayout
      break
    default:
    l = DefaultLayout
  }
  return l;
});

</script>

<template>

<component :is="layoutComponent">
  <router-view />
</component>

</template>


<style scoped>

</style>
