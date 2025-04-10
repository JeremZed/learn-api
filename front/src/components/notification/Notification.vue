<script setup>
import { ref, onMounted } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCheckCircle, faExclamationCircle, faExclamationTriangle, faInfoCircle } from '@fortawesome/free-solid-svg-icons';

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'info'
  },
  duration: {
    type: Number,
    default: 5000 // en ms
  },
  id: Number
});

const emit = defineEmits(['close']);

const icons = {
  success: faCheckCircle,
  error: faExclamationCircle,
  warning: faExclamationTriangle,
  info: faInfoCircle
};

onMounted(() => {
    if(props.duration > 0){
        setTimeout(() => emit('close', props.id), props.duration);
    }
});
const close = () => {
  emit('close', props.id);
};
</script>

<template>
  <div class="notification" :class="type" @click="close">
    <FontAwesomeIcon :icon="icons[type]" class="icon" />
    <span class="message">{{ message }}</span>
  </div>
</template>

<style scoped>
</style>
