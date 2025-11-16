<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-lg">
      <div class="flex flex-col h-full">
        <!-- Logo -->
        <div class="p-6 border-b">
          <h1 class="text-2xl font-bold text-primary-600">Sec-Llama</h1>
          <p class="text-sm text-gray-500 mt-1">Security Testing Suite</p>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="item.path"
            class="flex items-center px-4 py-3 text-gray-700 rounded-lg transition-colors hover:bg-primary-50 hover:text-primary-700"
            active-class="bg-primary-100 text-primary-700 font-medium"
          >
            <component :is="item.icon" class="w-5 h-5 mr-3" />
            <span>{{ item.label }}</span>
          </router-link>
        </nav>

        <!-- Footer -->
        <div class="p-4 border-t">
          <div class="flex items-center justify-between text-sm text-gray-500">
            <span>v1.0.0</span>
            <div class="flex items-center">
              <span
                :class="[
                  'w-2 h-2 rounded-full mr-2',
                  connected ? 'bg-green-500' : 'bg-red-500'
                ]"
              ></span>
              <span>{{ connected ? 'Connected' : 'Disconnected' }}</span>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useWebSocketStore } from '@/stores/websocket'
import {
  HomeIcon,
  WrenchScrewdriverIcon,
  Cog6ToothIcon,
  KeyIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

const wsStore = useWebSocketStore()

const navItems = [
  {
    name: 'dashboard',
    label: 'Dashboard',
    path: '/',
    icon: HomeIcon
  },
  {
    name: 'tools',
    label: 'Tools',
    path: '/tools',
    icon: WrenchScrewdriverIcon
  },
  {
    name: 'config',
    label: 'Configuration',
    path: '/config',
    icon: Cog6ToothIcon
  },
  {
    name: 'api-keys',
    label: 'API Keys',
    path: '/api-keys',
    icon: KeyIcon
  },
  {
    name: 'audit-logs',
    label: 'Audit Logs',
    path: '/audit-logs',
    icon: DocumentTextIcon
  }
]

const connected = computed(() => wsStore.connected)

onMounted(() => {
  // Connect to WebSocket
  wsStore.connect('/ws/dashboard')
})

onUnmounted(() => {
  wsStore.disconnect()
})
</script>
