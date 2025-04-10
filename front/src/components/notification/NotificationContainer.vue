<script setup>
import { ref } from 'vue';
import Notification from './Notification.vue';

const notifications = ref([]);

let counter = 0;

function showNotification(message, type = 'info', duration = 10000) {
  const id = counter++;
  notifications.value.push({ id, message, type, duration });
}

function closeNotification(id) {
  notifications.value = notifications.value.filter(n => n.id !== id);
}

defineExpose({ showNotification });
</script>

<template>
  <div class="notification-container">
    <Notification
      v-for="n in notifications"
      :key="n.id"
      :id="n.id"
      :message="n.message"
      :type="n.type"
      :duration="n.duration"
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
