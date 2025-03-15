<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  modelValue: Object, // État du formulaire
  fields: Array, // Liste des champs
  submitLabel: String, // Texte du bouton principal
  buttons: Array, // Liste des boutons supplémentaires avec leur action
});
const emit = defineEmits(["submit", "update:modelValue"]);

const updateField = (field, value) => {
  emit("update:modelValue", { ...props.modelValue, [field]: value });
};
</script>

<template>
  <form @submit.prevent="emit('submit', modelValue)">
    <div v-for="field in fields" :key="field.name">
      <label :for="field.name">{{ field.label }}</label>

      <!-- Champ texte / email / password -->
      <input
        v-if="['text', 'email', 'password'].includes(field.type)"
        :id="field.name"
        :type="field.type"
        :placeholder="field.placeholder"
        :value="modelValue[field.name]"
        @input="updateField(field.name, $event.target.value)"
      />

      <!-- Textarea -->
      <textarea
        v-else-if="field.type === 'textarea'"
        :id="field.name"
        :placeholder="field.placeholder"
        :value="modelValue[field.name]"
        @input="updateField(field.name, $event.target.value)"
      ></textarea>

      <!-- Select -->
      <select
        v-else-if="field.type === 'select'"
        :id="field.name"
        :value="modelValue[field.name]"
        @change="updateField(field.name, $event.target.value)"
      >
        <option disabled value="">Sélectionnez une option</option>
        <option v-for="option in field.options" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <!-- Checkbox -->
      <div v-else-if="field.type === 'checkbox'">
        <input
          type="checkbox"
          :id="field.name"
          :checked="modelValue[field.name]"
          @change="updateField(field.name, $event.target.checked)"
        />
        <label :for="field.name">{{ field.label }}</label>
      </div>
    </div>

    <!-- Bouton de soumission -->
    <button type="submit">{{ submitLabel }}</button>

    <!-- Boutons supplémentaires -->
    <button
      v-for="btn in buttons"
      :key="btn.label"
      type="button"
      @click="btn.action(modelValue)"
    >
      {{ btn.label }}
    </button>
  </form>
</template>
