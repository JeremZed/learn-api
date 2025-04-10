<!-- src/components/TopBar.vue -->
<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faUserShield, faSignOutAlt } from "@fortawesome/free-solid-svg-icons";


const props = defineProps({
  isAdmin: Boolean
});

const isMenuOpen = ref(false);
const userMenuRef = ref(null);
const emit = defineEmits(["logout"]);

const toggleMenuProfil = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};

const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    isMenuOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});
onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<template>
  <nav class="topnav shadow">
    <div></div>
    <div ref="userMenuRef" class="user-menu">
      <div class="user-avatar" @click="toggleMenuProfil">
        <font-awesome-icon :icon="faUser" />
      </div>

      <div v-if="isMenuOpen" class="dropdown-menu right">
        <router-link to="/profil" @click="closeMenu">
          <font-awesome-icon :icon="faUser" /> {{ $t("profile") }}
        </router-link>
        <router-link v-if="isAdmin" to="/admin" @click="closeMenu">
          <font-awesome-icon :icon="faUserShield" /> {{ $t("admin_panel") }}
        </router-link>
        <hr />
        <a href="#" @click="emit('logout')">
          <font-awesome-icon :icon="faSignOutAlt" /> {{ $t("logout") }}
        </a>
      </div>
    </div>
  </nav>
</template>
