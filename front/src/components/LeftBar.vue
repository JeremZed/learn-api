<script setup>
import {ref} from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faArrowRight, faArrowLeft, faCog, faHome } from "@fortawesome/free-solid-svg-icons";

const isCollapsed = ref(true);
const isMobileOpen = ref(false);

const toggleLeftMenu = () => {
    if (window.innerWidth <= 768) {
        isMobileOpen.value = !isMobileOpen.value;
    } else {
        isCollapsed.value = !isCollapsed.value;
    }
};

</script>


<template>
    <nav :class="['nav-leftbar', 'shadow', { collapsed: isCollapsed, open: isMobileOpen}]">
        <button @click="toggleLeftMenu" class="toggle-btn">
            <font-awesome-icon :icon="isMobileOpen ? faTimes : (isCollapsed ? faArrowRight : faArrowLeft)" />
        </button>

        <ul>
            <li class="menu-item logo"></li>
            <li class="menu-item">
                <router-link to="/">
                    <font-awesome-icon :icon="faHome" />
                    <span class="menu-text">{{ $t("nav_home") }}</span>
                </router-link>
            </li>
        </ul>
    </nav>
</template>