<template>
  <div id="app">
    <!-- <nav class="navbar">
      <router-link to="/">Accueil 123963</router-link> |
      <router-link to="/about">À propos</router-link>
    </nav> -->
    <nav>
    <div v-if="store.user">
      <p>Bienvenue, {{ store.user.username }}</p>
      <button @click="store.logout">Déconnexion</button>
    </div>
    <div v-else>
      <router-link to="/login">Connexion</router-link>
    </div>
  </nav>
    <!-- <div>
      <h2>Mises à jour du monde :</h2>
      <ul>
        <li v-for="(msg, index) in messages" :key="index">
          {{ msg }}
        </li>
      </ul>
    </div> -->
    <ThemeSwitcher />
    <router-view />
  </div>
</template>

<script setup>
import ThemeSwitcher from "@/components/ThemeSwitcher.vue";
import { store } from "@/store";

</script>

<style>
.navbar {
  padding: 20px;
  background-color: #f8f9fa;
}
.navbar a {
  margin: 0 10px;
  text-decoration: none;
  color: #2c3e50;
}
.navbar a.router-link-active {
  color: #42b983;
}
</style>
