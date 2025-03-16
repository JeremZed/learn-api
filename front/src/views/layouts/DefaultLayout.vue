<script setup>

import Switcher from "@/components/Switcher.vue";

</script>
<template>
    <div class="app-container">
        <main class="content">

            <Switcher />

            <div>Default Layout</div>

        <router-view />

        </main>
    </div>
</template>