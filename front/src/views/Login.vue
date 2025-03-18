<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { authService } from "@/services/authService.js";
import BaseForm from "@/components/forms/BaseForm.vue";

const router = useRouter();

const form = reactive({
  email: "",
  password: "",
});

const errorMessage = ref("");

const fields = [
  { name: "email", label: "Email", type: "email", placeholder: "Entrez votre email" },
  { name: "password", label: "Mot de passe", type: "password", placeholder: "Mot de passe" }
];

const handleSubmit = async (formData) => {
  try {
    await authService.login(formData.email, formData.password);
    router.push("/");
  } catch (error) {
    errorMessage.value = error;
  }
};

</script>

<template>
  <div class="login-container">
    <h2>Connexion</h2>
    <BaseForm v-model="form" :fields="fields" submitLabel="Se connecter" @submit="handleSubmit" />
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>

</style>
