<script setup>
import { ref } from 'vue';
import store from "@/stores/index.js";
import Notification from './Notification.vue';

const closeNotification = (id) => {
  store.notification.removeNotification(id);
};
</script>

<template>
  <div class="notification-container">
    <Notification
      v-for="n in store.notification.notifications"
      :key="n.id"
      :id="n.id"
      :message="n.message"
      :type="n.type"
      @close="closeNotification"
    />
  </div>
</template>

<style scoped>
.notification-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  width: 300px;
  z-index: 1000;
}
</style>
