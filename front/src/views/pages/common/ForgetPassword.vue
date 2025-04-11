<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useHead } from "@vueuse/head";
import { authService } from "@/services/authService.js";
import BaseForm from "@/components/forms/BaseForm.vue";

import store from "@/stores/index.js";

const { t } = useI18n();
const router = useRouter();

// SEO Meta
useHead({
  title: computed(() => t("seo_title_forget_password")),
  meta: [
    {
      name: "description",
      content: computed(() => t("seo_meta_description_forget_password"))
    }
  ]
});

// Champs du formulaire
const fields = computed(() => [
  { name: "email", label: t("email"), type: "email", placeholder: t("email_placeholder"), required: true },
]);

// Erreur à afficher en haut du formulaire
const errorMessage = ref("");

// Handler de soumission
const handleSubmit = async (formData) => {
  try {
    const response = await authService.sendQueryForgetPassword(formData.email).then(() => {
      store.notification.showNotification(t("query_send_success"), "success");
      router.push({ name: "login" });
    });

  } catch (error) {
    errorMessage.value = t(error.flag);
  }
};

// Callback optionnel après soumission réussie
const submitDone = (result) => {
  console.log(result);
};
</script>

<template>
  <div class="p-query-password-forget">
    <h1>{{ $t("forget_password") }}</h1>
    <BaseForm
      :fields="fields"
      :submitLabel="$t('send')"
      @submit="submitDone"
      :submitHandler="handleSubmit"
      :errorMessage="errorMessage"
      className="form-small shadow"
    />
    <div class="align-center">
      <div class="align-center"><router-link :to="{ name : 'login' }">{{ $t('already_account_?') }}</router-link></div>
    </div>
  </div>
</template>

<style scoped>

</style>
