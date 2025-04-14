<script setup>

import { computed } from "vue";
import store from "@/stores/index.js";
import TopBar from "@/components/TopBar.vue";
import LeftBar from "@/components/LeftBar.vue";
import NotificationContainer from '@/components/notification/NotificationContainer.vue';
import Breadcrumb from "@/components/Breadcrumb.vue"

const isAdmin = computed(() => store.user.isAdmin());
const isLogged = computed(() => store.user.user != null);

const logout = () => {
    store.user.logout();
};

</script>

<template>
    <div class="dashboard-wrapper">

        <LeftBar v-if="isLogged"  ></LeftBar>

        <div class="main">

            <TopBar v-if="isLogged" :isAdmin="isAdmin" @logout="logout" />
            <Breadcrumb />
            <main class="content">
                <router-view />
            </main>
            <NotificationContainer />

        </div>
    </div>

</template>