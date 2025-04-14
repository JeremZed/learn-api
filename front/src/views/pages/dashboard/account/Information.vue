<script setup>
import { useI18n } from "vue-i18n";
import { faLock, faCircleInfo } from '@fortawesome/free-solid-svg-icons';

import Card from "@/components/Card.vue"

const { t } = useI18n();
</script>

<template>
    <div class="p-information">
      <h1>{{ $t("page_information_title") }} </h1>
    </div>
</template>

<style scoped>

</style>