
<script setup>
import { ref } from "vue";

const message = ref("Welcome to my Vue application!");
const backendMessage = ref("");
const loading = ref(false);

const getBackendMessage = async () => {
  loading.value = true;
  backendMessage.value = "";

  try {
    const response = await fetch(
  `${import.meta.env.VITE_API_URL}/api/test`
);

    if (!response.ok) {
      throw new Error("Backend request failed");
    }

    const data = await response.json();

    backendMessage.value = data.message;
  } catch (error) {
    backendMessage.value = "Could not connect to backend!";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="container">
    <h1>{{ message }}</h1>

    <p>This is my first Vue 3 application.</p>

    <button @click="getBackendMessage" :disabled="loading">
      {{ loading ? "Loading..." : "Test Backend Connection" }}
    </button>

    <p v-if="backendMessage" class="message">
      {{ backendMessage }}
    </p>
  </main>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: 100px auto;
  padding: 30px;
  text-align: center;
  font-family: Arial, sans-serif;
}

h1 {
  color: #00bcd4;
}

button {
  background-color: #111;
  color: #00bcd4;
  border: 1px solid #00bcd4;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 20px;
}

button:hover {
  background-color: #222;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message {
  margin-top: 25px;
  color: #00bcd4;
}
</style>
