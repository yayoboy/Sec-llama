<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-500 mt-2">Overview of your security testing activities</p>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="dashboardStore.error" class="card bg-red-50 border border-red-200">
      <p class="text-red-800">Error loading dashboard: {{ dashboardStore.error }}</p>
    </div>

    <!-- Dashboard Content -->
    <div v-else-if="dashboardStore.hasData">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">Executions Today</p>
              <p class="text-3xl font-bold mt-1">{{ stats.total_executions_today }}</p>
            </div>
            <div class="p-3 bg-blue-100 rounded-lg">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">Active Executions</p>
              <p class="text-3xl font-bold mt-1">{{ stats.active_executions }}</p>
            </div>
            <div class="p-3 bg-green-100 rounded-lg">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">Available Tools</p>
              <p class="text-3xl font-bold mt-1">{{ stats.available_tools }}</p>
            </div>
            <div class="p-3 bg-purple-100 rounded-lg">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">System Status</p>
              <p class="text-lg font-bold mt-1">
                <span :class="[
                  'badge',
                  stats.ollama_status === 'running' ? 'badge-success' : 'badge-danger'
                ]">
                  {{ stats.ollama_status }}
                </span>
              </p>
            </div>
            <div class="p-3 bg-yellow-100 rounded-lg">
              <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Recent Executions -->
        <div class="card">
          <h2 class="text-xl font-bold mb-4">Recent Executions</h2>
          <div class="space-y-3">
            <div
              v-for="execution in dashboardStore.recentExecutions"
              :key="execution.execution_id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex-1">
                <p class="font-medium">{{ execution.tool_name }}</p>
                <p class="text-sm text-gray-500">
                  {{ formatDate(execution.started_at) }}
                </p>
              </div>
              <div class="flex items-center space-x-3">
                <span v-if="execution.duration" class="text-sm text-gray-500">
                  {{ execution.duration.toFixed(2) }}s
                </span>
                <span
                  :class="[
                    'badge',
                    execution.status === 'completed' ? 'badge-success' :
                    execution.status === 'running' ? 'badge-info' :
                    execution.status === 'failed' ? 'badge-danger' :
                    'badge-warning'
                  ]"
                >
                  {{ execution.status }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Tools -->
        <div class="card">
          <h2 class="text-xl font-bold mb-4">Top Tools</h2>
          <div class="space-y-3">
            <div
              v-for="tool in dashboardStore.topTools"
              :key="tool.tool_name"
              class="flex items-center justify-between"
            >
              <div class="flex-1">
                <p class="font-medium">{{ tool.tool_name }}</p>
                <div class="flex items-center mt-1">
                  <div class="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                    <div
                      class="bg-primary-600 h-2 rounded-full"
                      :style="{ width: `${tool.success_rate * 100}%` }"
                    ></div>
                  </div>
                  <span class="text-sm text-gray-500">
                    {{ (tool.success_rate * 100).toFixed(0) }}%
                  </span>
                </div>
              </div>
              <div class="ml-4 text-right">
                <p class="text-sm font-medium">{{ tool.execution_count }}</p>
                <p class="text-xs text-gray-500">executions</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500">No data available. Start executing tools to see statistics.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { useWebSocketStore } from '@/stores/websocket'

const dashboardStore = useDashboardStore()
const wsStore = useWebSocketStore()

const stats = computed(() => dashboardStore.stats || {
  total_executions_today: 0,
  active_executions: 0,
  available_tools: 0,
  ollama_status: 'unknown'
})

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString()
}

onMounted(async () => {
  await dashboardStore.fetchDashboardData()

  // Subscribe to real-time updates
  wsStore.subscribe('system_status', (data) => {
    if (data.status) {
      dashboardStore.stats = {
        ...dashboardStore.stats,
        ...data.status
      }
    }
  })

  wsStore.subscribe('tool_execution', () => {
    // Refresh dashboard data when tool execution updates
    dashboardStore.fetchDashboardData()
  })

  // Refresh data every 30 seconds
  setInterval(() => {
    dashboardStore.fetchStats()
  }, 30000)
})
</script>
