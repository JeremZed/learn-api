<script setup>
import { i18n, loadLocaleMessages } from "@/locales";

const changeLanguage = async (event) => {
  const newLocale = event.target.value;
  await loadLocaleMessages(newLocale);
};
</script>

<template>
  <div class="form-group">
    <label for="language-select">{{ $t("select_language") }} :</label>
    <select id="language-select" @change="changeLanguage" :value="i18n.global.locale.value">
      <option value="fr">{{ $t("language_fr") }}</option>
      <option value="en">{{ $t("language_en") }}</option>
    </select>
  </div>
</template>
