<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { faLock, faCircleInfo } from '@fortawesome/free-solid-svg-icons';
import store from "@/stores/index.js";

import Card from "@/components/Card.vue"
import BaseForm from "@/components/forms/BaseForm.vue";

import { accountService } from "@/services/accountService.js";

const { t } = useI18n();
const router = useRouter();

const fieldsChangePassword = computed(() => [
  { name: "current_password", label: t("current_password"), type: "password", placeholder: t("current_password_placeholder"), required: true },
  { name: "new_password", label: t("new_password"), type: "password", placeholder: t("new_password_placeholder"), required: true }
]);


// Erreur à afficher en haut du formulaire
const errorMessage = ref("");

// Handler de soumission du changement de mot de passe
const handleSubmitPassword = async (formData) => {
  return await accountService.changePassword(formData).then( (response) => {
      store.notification.showNotification(t('updated_success'), 'success')
      router.push({name:'account'});
      return response
    })

};

// Callback optionnel après soumission réussie
const submitDone = (result) => {
  console.log(result);
};

</script>

<template>
    <div class="p-security">

      <h1>{{ $t("page_security_title") }} </h1>

      <Card
            :title="t('change_password')"
            :description="t('description_change_password')"
            :icon="faCircleInfo"
          >
          <BaseForm
            :fields="fieldsChangePassword"
            :submitLabel="$t('update')"
            @submit="submitDone"
            :submitHandler="handleSubmitPassword"
            className=""
            :buttons="[{label : 'Annuler', class : 'btn-error', action : (datas) => { router.push({name:'account'}); }}]"
          />
      </Card>

    </div>
</template>

<style scoped>

</style>