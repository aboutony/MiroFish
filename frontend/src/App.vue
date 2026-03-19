<template>
  <div :class="currentTheme" class="min-h-screen transition-colors duration-500">
    <nav class="p-4 border-b flex justify-between items-center bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-800 shadow-sm">
      <div class="flex items-center gap-2">
        <div class="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-xs">MF</span>
        </div>
        <span class="text-lg font-bold tracking-tight text-slate-800 dark:text-slate-100">MARKET PREDICTOR</span>
      </div>
      
      <div class="flex items-center gap-6">
        <button @click="toggleTheme" class="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-all border border-transparent hover:border-slate-200 dark:hover:border-slate-700">
          <span v-if="currentTheme === 'light'" class="text-xl">🌙</span>
          <span v-else class="text-xl">☀️</span>
        </button>
        
        <div class="flex items-center gap-3 pl-4 border-l border-slate-200 dark:border-slate-700">
          <span class="text-sm font-medium text-slate-600 dark:text-slate-400">Strategist</span>
          <div class="h-9 w-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-white dark:ring-slate-900">
            AD
          </div>
        </div>
      </div>
    </nav>

    <main class="container mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { applyTheme, getSavedTheme } from './utils/theme_manager';

const currentTheme = ref(getSavedTheme());

const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light';
  applyTheme(currentTheme.value);
};

onMounted(() => {
  applyTheme(currentTheme.value);
});
</script>

<style>
/* Base Dark Mode Support */
.dark body {
  background-color: #0f172a;
}
</style>
