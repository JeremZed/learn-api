<script setup>
import { ref } from "vue";
import ThemeSwitcher from "@/components/switchers/ThemeSwitcher.vue";
import ModeSwitcher from "@/components/switchers/ModeSwitcher.vue";
import LayoutSwitcher from "@/components/switchers/LayoutSwitcher.vue";
import LanguageSwitcher from "@/components/switchers/LanguageSwitcher.vue";

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faGear, faXmark } from '@fortawesome/free-solid-svg-icons';


const isOpen = ref(false)
</script>

<template>
    <div :class="['switchers', {open:isOpen, shadow:isOpen}]">
        <div class="toggle-btn" @click="isOpen = !isOpen">
            <font-awesome-icon v-if="isOpen" :icon="faXmark" />
            <font-awesome-icon v-else :icon="faGear" />
        </div>

        <h2>Configurateur</h2>
        <div class="form">
            <ThemeSwitcher />
            <ModeSwitcher />
            <LayoutSwitcher />
            <LanguageSwitcher />
        </div>
    </div>
</template>