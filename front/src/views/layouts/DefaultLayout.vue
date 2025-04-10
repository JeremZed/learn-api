<script setup>

import { ref, computed, onMounted, onUnmounted } from "vue";

import Switcher from "@/components/Switcher.vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faSignOutAlt, faCog, faUserShield, faArrowDown, faArrowUp } from "@fortawesome/free-solid-svg-icons";
import store from "@/stores/index.js";


const isOpen = ref(false)
const isMenuOpen = ref(false);
const isAdmin = computed(() => store.user.isAdmin());
const userMenuRef = ref(null);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const logout = () => {
    isMenuOpen.value = false
    store.user.logout();
};

const closeMenu = () => {
    isMenuOpen.value = false;
};

// Permet de gérer la fermeture automatique du menu si l'utilisateur clique en dehors du menu
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
    <div class="wrapper">

        <nav class="navbar shadow">
            <div :class="['flex', {open:isOpen}]">
                <div class="flex col-8 flex-space-evently">
                    <router-link to="/">{{ $t("nav_home") }}</router-link>
                    <router-link to="/about">{{ $t("nav_about") }}</router-link>
                    <router-link to="/services">{{ $t("nav_service") }}</router-link>
                    <router-link to="/contact">{{ $t("nav_contact") }}</router-link>
                </div>

                <div v-if="!store.user.isAuthenticated" class="flex flex-center col-4">
                    <router-link to="/login" class="btn">{{ $t("signin") }}</router-link>
                </div>
                <div v-else ref="userMenuRef" class="user-menu">
                    <div class="user-avatar" @click="toggleMenu">
                        <font-awesome-icon :icon="faUser" />
                    </div>

                    <div v-if="isMenuOpen" class="dropdown-menu">
                        <router-link to="/profil" @click="closeMenu">
                            <font-awesome-icon :icon="faUser" /> {{ $t("profile") }}
                        </router-link>
                        <router-link v-if="isAdmin" to="/admin" @click="closeMenu">
                            <font-awesome-icon :icon="faUserShield" /> {{ $t("admin_panel") }}
                        </router-link>
                        <hr />
                        <a href="#" @click="logout">
                            <font-awesome-icon :icon="faSignOutAlt" /> {{ $t("logout") }}
                        </a>
                    </div>
                </div>
            </div>
            <div class="show-navbar-mobile" @click="isOpen = !isOpen">
                <font-awesome-icon v-if="isOpen" :icon="faArrowUp" />
                <font-awesome-icon v-else :icon="faArrowDown" />
            </div>


        </nav>

        <main class="content">

            <Switcher />

        <router-view />

        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />

        <p>hELLO</p>

        </main>
    </div>
</template>