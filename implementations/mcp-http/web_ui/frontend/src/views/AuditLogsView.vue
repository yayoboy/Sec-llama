<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Audit Logs</h1>
      <p class="text-gray-500 mt-2">View and filter security tool execution logs</p>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <h2 class="text-lg font-bold mb-4">Filters</h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Tool Name</label>
          <select v-model="filters.tool_name" class="input w-full" @change="applyFilters">
            <option value="">All Tools</option>
            <option value="network_discover">network_discover</option>
            <option value="network_scan">network_scan</option>
            <option value="code_scan">code_scan</option>
            <option value="threat_cve_lookup">threat_cve_lookup</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
          <select v-model="filters.status" class="input w-full" @change="applyFilters">
            <option value="">All Statuses</option>
            <option value="success">Success</option>
            <option value="failed">Failed</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
          <input
            v-model="filters.start_date"
            type="datetime-local"
            class="input w-full"
            @change="applyFilters"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
          <input
            v-model="filters.end_date"
            type="datetime-local"
            class="input w-full"
            @change="applyFilters"
          />
        </div>
      </div>

      <div class="mt-4 flex justify-between items-center">
        <button @click="resetFilters" class="btn-secondary">
          Reset Filters
        </button>
        <div class="flex space-x-2">
          <button @click="exportLogs('json')" class="btn-secondary">
            Export JSON
          </button>
          <button @click="exportLogs('csv')" class="btn-secondary">
            Export CSV
          </button>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div v-if="stats" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="card">
        <p class="text-gray-500 text-sm">Total Entries</p>
        <p class="text-3xl font-bold mt-1">{{ stats.total_entries }}</p>
      </div>

      <div class="card">
        <p class="text-gray-500 text-sm">Success Rate</p>
        <p class="text-3xl font-bold mt-1">
          {{ ((stats.successful_executions / stats.total_entries) * 100).toFixed(1) }}%
        </p>
      </div>

      <div class="card">
        <p class="text-gray-500 text-sm">Average Duration</p>
        <p class="text-3xl font-bold mt-1">{{ stats.average_duration.toFixed(2) }}s</p>
      </div>
    </div>

    <!-- Audit Logs Table -->
    <div class="card">
      <div v-if="logs.length > 0" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Timestamp
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tool
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Duration
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                IP Address
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="log in logs" :key="log.timestamp">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatDate(log.timestamp) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ log.tool_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'badge',
                  log.status === 'success' || log.status === 'completed' ? 'badge-success' :
                  log.status === 'failed' || log.status === 'error' ? 'badge-danger' :
                  'badge-warning'
                ]">
                  {{ log.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ log.duration ? log.duration.toFixed(2) + 's' : 'N/A' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ log.ip_address || 'N/A' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <button
                  @click="viewDetails(log)"
                  class="text-primary-600 hover:text-primary-900"
                >
                  Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center py-12">
        <p class="text-gray-500">No audit logs found</p>
      </div>
    </div>

    <!-- Log Details Modal -->
    <div
      v-if="selectedLog"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="selectedLog = null"
    >
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
        <h2 class="text-2xl font-bold mb-4">Audit Log Details</h2>

        <div class="space-y-3">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Tool Name</p>
              <p class="font-medium">{{ selectedLog.tool_name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Status</p>
              <span :class="[
                'badge',
                selectedLog.status === 'success' || selectedLog.status === 'completed' ? 'badge-success' :
                selectedLog.status === 'failed' || selectedLog.status === 'error' ? 'badge-danger' :
                'badge-warning'
              ]">
                {{ selectedLog.status }}
              </span>
            </div>
            <div>
              <p class="text-sm text-gray-500">Timestamp</p>
              <p class="font-medium">{{ formatDate(selectedLog.timestamp) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Duration</p>
              <p class="font-medium">{{ selectedLog.duration ? selectedLog.duration.toFixed(2) + 's' : 'N/A' }}</p>
            </div>
          </div>

          <div v-if="selectedLog.parameters">
            <p class="text-sm text-gray-500 mb-2">Parameters</p>
            <pre class="bg-gray-50 p-3 rounded text-sm overflow-x-auto">{{ JSON.stringify(selectedLog.parameters, null, 2) }}</pre>
          </div>

          <div v-if="selectedLog.error">
            <p class="text-sm text-gray-500 mb-2">Error</p>
            <div class="bg-red-50 border border-red-200 p-3 rounded text-sm text-red-800">
              {{ selectedLog.error }}
            </div>
          </div>
        </div>

        <div class="mt-6 flex justify-end">
          <button @click="selectedLog = null" class="btn-secondary">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/client'

const logs = ref([])
const stats = ref(null)
const loading = ref(false)
const selectedLog = ref(null)

const filters = ref({
  tool_name: '',
  status: '',
  start_date: '',
  end_date: '',
  limit: 100
})

async function loadLogs() {
  loading.value = true
  try {
    const params = {}

    if (filters.value.tool_name) params.tool_name = filters.value.tool_name
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.start_date) params.start_date = new Date(filters.value.start_date).toISOString()
    if (filters.value.end_date) params.end_date = new Date(filters.value.end_date).toISOString()
    if (filters.value.limit) params.limit = filters.value.limit

    const response = await api.getAuditLogs(params)
    logs.value = response.data
  } catch (error) {
    console.error('Failed to load audit logs:', error)
  } finally {
    loading.value = false
  }
}

async function loadStats() {
  try {
    const response = await api.getAuditLogStats(7)
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

function applyFilters() {
  loadLogs()
}

function resetFilters() {
  filters.value = {
    tool_name: '',
    status: '',
    start_date: '',
    end_date: '',
    limit: 100
  }
  loadLogs()
}

async function exportLogs(format) {
  try {
    const response = await api.exportAuditLogs(format, 30)
    const data = response.data

    if (format === 'json') {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      downloadBlob(blob, 'audit_logs.json')
    } else if (format === 'csv') {
      const blob = new Blob([data.data], { type: 'text/csv' })
      downloadBlob(blob, 'audit_logs.csv')
    }
  } catch (error) {
    console.error('Failed to export logs:', error)
    alert('Failed to export logs')
  }
}

function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

function viewDetails(log) {
  selectedLog.value = log
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}

onMounted(async () => {
  await Promise.all([loadLogs(), loadStats()])
})
</script>
