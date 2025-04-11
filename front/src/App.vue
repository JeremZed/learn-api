
<script setup>

import DefaultLayout from "@/views/layouts/DefaultLayout.vue";
import SecondLayout from "@/views/layouts/SecondLayout.vue";
import DashboardLayout from "@/views/layouts/DashboardLayout.vue";


import { LAYOUTS } from "@/constants.js";

import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import store from "@/stores/index.js";

const router = useRouter();

const layoutComponent = computed(() => {
  let l;

  // switch (store.switcher.layout) {
  //   case LAYOUTS.DEFAULT:
  //     l = DefaultLayout
  //     break;
  //   case LAYOUTS.SECOND:
  //     l = SecondLayout
  //     break
  //   case LAYOUTS.DASHBOARD:
  //     l = DashboardLayout
  //     break
  //   default:
  //   l = DashboardLayout
  // }
  return DashboardLayout;
});

onMounted(async () => {
  await store.user.init()
  .then(() => { router.push("/"); })
  .catch( () => {
    // router.push('/login')
  });
});

</script>

<template>

<component :is="layoutComponent">
  <router-view />
</component>

</template>


<style scoped>

</style>
