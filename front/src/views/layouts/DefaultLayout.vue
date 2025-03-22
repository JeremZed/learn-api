<script setup>

import { ref } from "vue";

import Switcher from "@/components/Switcher.vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faArrowDown, faArrowUp } from '@fortawesome/free-solid-svg-icons';

const isOpen = ref(false)
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
                <div class="flex flex-center col-4">
                    <a href="" class="btn">{{ $t("signin") }}</a>
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