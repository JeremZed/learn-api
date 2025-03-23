<script setup>
import { reactive, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useHead } from "@vueuse/head";
import { authService } from "@/services/authService.js";
import BaseForm from "@/components/forms/BaseForm.vue";
import store from "@/stores/index.js";

const { t } = useI18n();
const router = useRouter();

// Modification du title de la page
useHead({
  title: computed(() => t("seo_title_login")),
  meta: [
    {
      name: "description",
      content: computed(() => t("seo_meta_description_login"))
    }
  ]
});

const form = reactive({
  email: "",
  password: "",
});

const errorMessage = ref("");

const fields = computed(() =>  [
  { name: "email", label: t('email'), type: "email", placeholder: t('email_placeholder') },
  { name: "password", label: t('password'), type: "password", placeholder: t('password_placeholder') }
]);

const handleSubmit = async (formData) => {
  try {
    await authService.login(formData.email, formData.password).then((response) => {

      if( typeof response?.data?.token != "undefined"){
        store.user.setUser(response.data.user, response.data.token);
        router.push("/");
      }
    })

  } catch (error) {
    errorMessage.value = error;
  }
};

</script>

<template>
  <div class="login-container">
    <h1>{{ $t("connexion") }}</h1>
    <BaseForm
    v-model="form"
    :fields="fields"
    :submitLabel="$t('signin')"
    @submit="handleSubmit"
    className="form-login shadow"
    :errorMessage="errorMessage"
     />

  </div>
</template>

<style scoped>

</style>
