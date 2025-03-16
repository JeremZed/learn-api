<script setup>
import { i18n, loadLocaleMessages } from "@/locales";

const changeLanguage = async (event) => {
  const newLocale = event.target.value;
  await loadLocaleMessages(newLocale);
};
</script>

<template>
  <div class="language-switcher">
    <label for="language-select">{{ $t("language") }} :</label>
    <select id="language-select" @change="changeLanguage" :value="i18n.global.locale.value">
      <option value="fr">Français</option>
      <option value="en">English</option>
    </select>
  </div>
</template>
