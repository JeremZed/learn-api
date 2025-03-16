<script setup>

import Switcher from "@/components/Switcher.vue";

</script>
<template>
    <div class="app-container">
        <main class="content">

            <div>Second Layout</div>

        <router-view />
        <Switcher />
        </main>
    </div>
</template>