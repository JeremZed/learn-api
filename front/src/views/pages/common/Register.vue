<script setup>
import { reactive, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useHead } from "@vueuse/head";
import { authService } from "@/services/authService.js";
import BaseForm from "@/components/forms/BaseForm.vue";
import NotificationContainer from '@/components/notification/NotificationContainer.vue';


import store from "@/stores/index.js";
import { LAYOUTS } from "@/constants.js";

const { t } = useI18n();
const router = useRouter();
const notificationRef = ref();

// Meta
useHead({
  title: computed(() => t("seo_title_register")),
  meta: [
    {
      name: "description",
      content: computed(() => t("seo_meta_description_register"))
    }
  ]
});

// Initialisation des champs du formulaire
const fields = computed(() =>  [
  { name: "email", label: t('email'), type: "text", placeholder: t('email_placeholder'), required : true },
  { name: "username", label: t('username'), type: "text", placeholder: t('username_placeholder'), required : true },
  { name: "password", label: t('password'), type: "password", placeholder: t('password_placeholder'), required : true }
]);


// Callback à lancer lors de la soumission du formulaire
const handleSubmit = async (formData) => {
      return await authService.register(formData).then( (response) => {
        notificationRef.value.showNotification(t('signup_success'), 'success')
        return response
      })
    //   .then((response) => {
    //   // if( typeof response?.data?.token != "undefined"){
    //   //   store.user.setUser(response.data.user, response.data.token);
    //   //   store.switcher.setLayout(LAYOUTS.DASHBOARD);
    //   //   router.push("/");
    //   // }
    //   // console.log(response)
    //   return response
    // })
};

// Callback à lancer une fois que le formulaire a été soumis avec succès
const submitDone = (result) => { console.log(result) }

</script>

<template>
  <div class="p-register">
    <h1>{{ $t("register") }}</h1>
    <BaseForm
    :fields="fields"
    :submitLabel="$t('submit')"
    @submit="submitDone"
    :submitHandler="handleSubmit"
    className="form-small shadow"
     />
     <NotificationContainer ref="notificationRef" />
     <div class="align-center"><router-link to="/login">{{ $t('already_account_?') }}</router-link></div>
  </div>
</template>

<style scoped>

</style>
