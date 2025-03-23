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
                    <a href="#" class="">{{ $t("nav_home") }}</a>
                    <a href="#" class="">{{ $t("nav_about") }}</a>
                    <a href="#" class="">{{ $t("nav_service") }}</a>
                    <a href="#" class="">{{ $t("nav_contact") }}</a>
                </div>

                <div v-if="!store.user.isAuthenticated" class="flex flex-center col-4">
                    <a href="" class="btn">{{ $t("signin") }}</a>
                </div>
                <div v-else ref="userMenuRef" class="user-menu">
                    <div class="user-avatar" @click="toggleMenu">
                        <font-awesome-icon :icon="faUser" />
                    </div>

                    <div v-if="isMenuOpen" class="dropdown-menu">
                        <router-link to="/about" @click="closeMenu">
                            <font-awesome-icon :icon="faUser" /> {{ $t("profile") }}
                        </router-link>
                        <router-link to="/about" @click="closeMenu">
                            <font-awesome-icon :icon="faCog" /> {{ $t("settings") }}
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