<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useHead } from "@vueuse/head";
import { authService } from "@/services/authService.js";
import BaseForm from "@/components/forms/BaseForm.vue";

import store from "@/stores/index.js";
import { LAYOUTS } from "@/constants.js";

const { t } = useI18n();
const router = useRouter();

// SEO Meta
useHead({
  title: computed(() => t("seo_title_login")),
  meta: [
    {
      name: "description",
      content: computed(() => t("seo_meta_description_login"))
    }
  ]
});

// Champs du formulaire
const fields = computed(() => [
  { name: "email", label: t("email"), type: "email", placeholder: t("email_placeholder"), required: true },
  { name: "password", label: t("password"), type: "password", placeholder: t("password_placeholder"), required: true }
]);

// Erreur à afficher en haut du formulaire
const errorMessage = ref("");

// Handler de soumission
const handleSubmit = async (formData) => {
  try {
    const response = await authService.login(formData.email, formData.password);
    console.log(response)
    if (response?.data?.user) {
      store.user.setUser(response.data.user);
      store.notification.showNotification(t("login_success"), "success");
      router.push("/");
    }
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
  <div class="p-login">
    <h1>{{ $t("connexion") }}</h1>
    <BaseForm
      :fields="fields"
      :submitLabel="$t('signin')"
      @submit="submitDone"
      :submitHandler="handleSubmit"
      :errorMessage="errorMessage"
      className="form-small shadow"
    />
    <div class="align-center">
      <router-link to="/register">{{ $t("not_account_?") }}</router-link>
    </div>
  </div>
</template>

<style scoped>

</style>
