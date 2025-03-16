<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api.js";
import store from "@/stores/index.js";

const router = useRouter();

// État réactif pour les champs du formulaire
const form = reactive({
  email: "",
  password: "",
});

const errorMessage = ref("");

const login = async () => {
  errorMessage.value = "";

  try {
        const response = await api.post("/auth/login", {
            email : form.email,
            password : form.password
        });

        const data = response.data;

        if (!response.status === 200) {
            throw new Error(data.detail || "Échec de l'authentification");
        }

        // Stocker l'utilisateur dans le store
        store.user.setUser(null, data.data);

        // Redirection après connexion
        router.push("/");
    } catch (error) {
        errorMessage.value = error.response?.data?.detail || "Connexion échouée.";
    }
};
</script>

<template>
  <div class="login-container">
    <h2>Connexion</h2>
    <form @submit.prevent="login">
      <div>
        <label for="email">Nom d'utilisateur :</label>
        <input v-model="form.email" type="text" id="email" required />
      </div>

      <div>
        <label for="password">Mot de passe :</label>
        <input v-model="form.password" type="password" id="password" required />
      </div>

      <button type="submit">Se connecter</button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 8px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
