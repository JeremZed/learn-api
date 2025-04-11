// stores/notificationStore.js
import { reactive } from 'vue';

let idCounter = 0;

export const notificationStore = reactive({
  notifications: [],

  showNotification(message, type = 'info', duration = 5000) {
    const id = idCounter++;
    this.notifications.push({ id, message, type, duration });

    if (duration > 0) {
      setTimeout(() => this.removeNotification(id), duration);
    }
  },

  removeNotification(id) {
    this.notifications = this.notifications.filter(n => n.id !== id);
  }
});
