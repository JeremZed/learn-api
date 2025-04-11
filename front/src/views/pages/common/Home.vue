<script setup>

// HOME PAGE
import { computed, ref } from "vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCoffee } from '@fortawesome/free-solid-svg-icons';
import { useI18n } from "vue-i18n";
import { useHead } from "@vueuse/head";

const { t } = useI18n();

  // SEO Meta
useHead({
  title: computed(() => t("seo_title_dashboard")),
  meta: [
    {
      name: "description",
      content: computed(() => t("seo_meta_description_dashboard"))
    }
  ]
});

</script>

<template>
    <div class="p-home">
      <h1>{{ $t("welcome") }} <font-awesome-icon :icon="faCoffee" /> </h1>

    </div>
</template>

<style scoped>
  /** CSS **/
</style>