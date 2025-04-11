<script setup>
import { defineProps, defineEmits, reactive, watchEffect } from "vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';

// Définition des paramètres du composanant
const props = defineProps({
  fields: Array,
  submitLabel: String,
  buttons: Array,
  className: String,
  id: String,
  submitHandler: Function,
  errorMessage: String
});

// Défintion des events à émettre
const emit = defineEmits(["submit", "update:modelValue"]);

// Modèle représentant les données du formulaire
const modelValue = reactive({});

// Initialisation des variables en fonction des champs du formulaire
watchEffect(() => {

  props.fields.forEach(field => {
    if (modelValue[field.name] === undefined) {
      modelValue[field.name] = field.value || '';
    }
  });
});

// Dictionnaire des champs en erreur
let fieldErrors = reactive({});

// Fonction de mise à jour du modèle des données du formulaire
const updateField = (field, value) => {
  modelValue[field] = value;
};

// Fonction principale de soumission du formulaire
const handleSubmit = (e) => {

  e.preventDefault();

  // Si on souhaite un comportement personnalisé à la soumission (par exemple un appel API..)
  if (props.submitHandler) {

    props.submitHandler(modelValue)

      // une fois le callback exécuté on émet l'event
      .then((response) => {
        Object.keys(fieldErrors).forEach((key) => fieldErrors[key] = "");
        Object.keys(modelValue).forEach((key) => modelValue[key] = '');
        emit("submit", { "values" : {...modelValue}, "response" : response });
      })
      // Gestion de l'affichage des erreurs de formulaire
      .catch((error) => {

        console.error("Submission failed:", error);

        if (error?.flag === "form_value_error") {
          Object.keys(fieldErrors).forEach((key) => fieldErrors[key] = "");
          for (const err of error.data) {
            fieldErrors[err.field] = err.msg;
          }
        }
      });

  } else {
    // Sinon on retourne uniquement les données du formulaire
    emit("submit", { "values" : {...modelValue} });
  }
};

</script>

<template>
  <form @submit.prevent="handleSubmit" :class="['form', className]" :id="id" >


    <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>

    <div v-for="field in fields" :key="field.name" class="form-group">
      <label :for="field.name">{{ field.label }}</label>

      <!-- Champ texte / email / password -->
      <div class="input-wrapper">
        <input
          v-if="['text', 'email', 'password'].includes(field.type)"
          :id="field.name"
          :type="field.type"
          :placeholder="field.placeholder"
          :value="modelValue[field.name]"
          @input="updateField(field.name, $event.target.value);"
          :required="field.required"
          :class="{'input-error': fieldErrors?.[field.name]}"
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

        <span class="input-error-icon " v-if="fieldErrors?.[field.name]">
          <font-awesome-icon :icon="faTriangleExclamation" />
        </span>


      </div>

        <div v-if="fieldErrors?.[field.name]" class="form-error">
          {{ fieldErrors[field.name] }}
        </div>
    </div>

    <div class="form-group">
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
    </div>
  </form>
</template>
