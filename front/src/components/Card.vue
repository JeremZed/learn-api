<script setup>

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

    defineProps({
    title: String,
    description: String,
    icon: Object,
    actions: Array
    })

</script>

<template>
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">
            <span class="card-icon" v-if="icon">
                <font-awesome-icon :icon="icon" />
            </span>
            {{ title }}
        </h2>
        <p class="card-description">{{ description }}</p>
      </div>
      <div class="card-content">
        <slot />
      </div>
      <div v-if="actions" class="card-actions">
        <div v-for="action in actions" :key="action.to">
            <router-link :to="{ name: action.to }" class="btn" >{{ action.label }}</router-link>
        </div>
      </div>
    </div>
</template>

