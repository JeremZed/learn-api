<script setup>
  // HOME PAGE

  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faCoffee } from '@fortawesome/free-solid-svg-icons';


</script>

<template>
    <div class="p-home">
      <h1>{{ $t("welcome") }} <font-awesome-icon :icon="faCoffee" /> </h1>

    </div>
</template>

<style scoped>
  /** CSS **/
</style>