<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Configuration</h1>
        <p class="text-gray-500 mt-2">Manage MCP server configuration</p>
      </div>
      <div class="flex space-x-3">
        <button @click="downloadConfig" class="btn-secondary">
          Download
        </button>
        <button @click="createBackup" class="btn-secondary">
          Create Backup
        </button>
        <button @click="loadConfig" class="btn-secondary">
          Reload
        </button>
        <button
          @click="saveConfig"
          class="btn-primary"
          :disabled="saving || !hasChanges"
        >
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>

    <!-- Validation Errors -->
    <div v-if="validationErrors.length > 0" class="card bg-red-50 border border-red-200 mb-6">
      <h3 class="font-bold text-red-900 mb-2">Validation Errors</h3>
      <ul class="list-disc list-inside text-red-800 text-sm space-y-1">
        <li v-for="(error, index) in validationErrors" :key="index">{{ error }}</li>
      </ul>
    </div>

    <!-- Validation Warnings -->
    <div v-if="validationWarnings.length > 0" class="card bg-yellow-50 border border-yellow-200 mb-6">
      <h3 class="font-bold text-yellow-900 mb-2">Warnings</h3>
      <ul class="list-disc list-inside text-yellow-800 text-sm space-y-1">
        <li v-for="(warning, index) in validationWarnings" :key="index">{{ warning }}</li>
      </ul>
    </div>

    <!-- Configuration Editor -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- YAML Editor -->
      <div class="card">
        <h2 class="text-xl font-bold mb-4">Configuration (YAML)</h2>
        <div class="mb-3 flex justify-between items-center">
          <span class="text-sm text-gray-500">Last modified: {{ lastModified }}</span>
          <button @click="validateConfig" class="btn-secondary text-sm">
            Validate
          </button>
        </div>
        <textarea
          v-model="configYaml"
          class="input w-full font-mono text-sm"
          rows="25"
          :disabled="loading"
          @input="markAsChanged"
        ></textarea>
      </div>

      <!-- Configuration Info -->
      <div class="space-y-6">
        <!-- Current Config Summary -->
        <div class="card">
          <h3 class="text-lg font-bold mb-4">Configuration Summary</h3>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">Server Name:</span>
              <span class="font-medium">{{ configData?.server?.name || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Version:</span>
              <span class="font-medium">{{ configData?.server?.version || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">STDIO Enabled:</span>
              <span :class="configData?.transport?.stdio?.enabled ? 'text-green-600' : 'text-red-600'">
                {{ configData?.transport?.stdio?.enabled ? 'Yes' : 'No' }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">HTTP Enabled:</span>
              <span :class="configData?.transport?.http?.enabled ? 'text-green-600' : 'text-red-600'">
                {{ configData?.transport?.http?.enabled ? 'Yes' : 'No' }}
              </span>
            </div>
            <div v-if="configData?.transport?.http?.enabled" class="flex justify-between">
              <span class="text-gray-600">HTTP Port:</span>
              <span class="font-medium">{{ configData?.transport?.http?.port || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Auth Type:</span>
              <span class="font-medium">{{ configData?.auth?.type || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Rate Limiting:</span>
              <span :class="configData?.rate_limiting?.enabled ? 'text-green-600' : 'text-red-600'">
                {{ configData?.rate_limiting?.enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Backups -->
        <div class="card">
          <h3 class="text-lg font-bold mb-4">Backups</h3>
          <div v-if="backups.length > 0" class="space-y-2 max-h-64 overflow-y-auto">
            <div
              v-for="backup in backups"
              :key="backup.backup_id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded"
            >
              <div>
                <p class="text-sm font-medium">{{ backup.backup_id }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(backup.created_at) }}</p>
              </div>
              <button
                @click="restoreBackup(backup.backup_id)"
                class="btn-secondary text-xs"
              >
                Restore
              </button>
            </div>
          </div>
          <p v-else class="text-sm text-gray-500">No backups available</p>
        </div>

        <!-- Configuration Schema Helper -->
        <div class="card">
          <h3 class="text-lg font-bold mb-4">Configuration Schema</h3>
          <p class="text-sm text-gray-600 mb-3">
            Need help with configuration? View the schema to see all available options.
          </p>
          <button @click="showSchema" class="btn-secondary w-full">
            View Schema
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/client'
import yaml from 'js-yaml'

const loading = ref(false)
const saving = ref(false)
const configYaml = ref('')
const originalYaml = ref('')
const lastModified = ref('')
const backups = ref([])
const validationErrors = ref([])
const validationWarnings = ref([])

const configData = computed(() => {
  try {
    return yaml.load(configYaml.value)
  } catch (e) {
    return null
  }
})

const hasChanges = computed(() => {
  return configYaml.value !== originalYaml.value
})

function markAsChanged() {
  // Triggered when user edits the config
}

async function loadConfig() {
  loading.value = true
  validationErrors.value = []
  validationWarnings.value = []

  try {
    const response = await api.getConfiguration()
    const data = response.data

    // Convert config data to YAML
    configYaml.value = yaml.dump(data.config_data, {
      indent: 2,
      lineWidth: -1
    })
    originalYaml.value = configYaml.value

    lastModified.value = new Date(data.last_modified).toLocaleString()
  } catch (error) {
    console.error('Failed to load configuration:', error)
  } finally {
    loading.value = false
  }
}

async function saveConfig() {
  saving.value = true
  validationErrors.value = []
  validationWarnings.value = []

  try {
    // Parse YAML first
    const configData = yaml.load(configYaml.value)

    // Validate before saving
    const validation = await api.validateConfiguration(configData)

    if (!validation.data.valid) {
      validationErrors.value = validation.data.errors
      validationWarnings.value = validation.data.warnings
      return
    }

    // Save configuration
    await api.updateConfiguration(configData, true)

    originalYaml.value = configYaml.value
    validationWarnings.value = validation.data.warnings

    alert('Configuration saved successfully!')
  } catch (error) {
    if (error.name === 'YAMLException') {
      validationErrors.value = [`YAML parsing error: ${error.message}`]
    } else {
      console.error('Failed to save configuration:', error)
      alert('Failed to save configuration')
    }
  } finally {
    saving.value = false
  }
}

async function validateConfig() {
  validationErrors.value = []
  validationWarnings.value = []

  try {
    const configData = yaml.load(configYaml.value)
    const response = await api.validateConfiguration(configData)

    if (response.data.valid) {
      alert('Configuration is valid!')
    }

    validationErrors.value = response.data.errors
    validationWarnings.value = response.data.warnings
  } catch (error) {
    if (error.name === 'YAMLException') {
      validationErrors.value = [`YAML parsing error: ${error.message}`]
    } else {
      console.error('Validation failed:', error)
    }
  }
}

async function createBackup() {
  try {
    await api.createBackup()
    await loadBackups()
    alert('Backup created successfully!')
  } catch (error) {
    console.error('Failed to create backup:', error)
    alert('Failed to create backup')
  }
}

async function loadBackups() {
  try {
    const response = await api.listBackups()
    backups.value = response.data
  } catch (error) {
    console.error('Failed to load backups:', error)
  }
}

async function restoreBackup(backupId) {
  if (!confirm(`Are you sure you want to restore backup ${backupId}?`)) {
    return
  }

  try {
    await api.restoreBackup(backupId)
    await loadConfig()
    alert('Backup restored successfully!')
  } catch (error) {
    console.error('Failed to restore backup:', error)
    alert('Failed to restore backup')
  }
}

async function downloadConfig() {
  try {
    const response = await api.downloadConfiguration()
    const blob = new Blob([response.data], { type: 'application/x-yaml' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'mcp_server_config.yaml'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (error) {
    console.error('Failed to download configuration:', error)
  }
}

async function showSchema() {
  try {
    const response = await api.getConfigurationSchema()
    const schemaYaml = yaml.dump(response.data, { indent: 2 })
    alert(`Configuration Schema:\n\n${schemaYaml}`)
  } catch (error) {
    console.error('Failed to load schema:', error)
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}

onMounted(async () => {
  await loadConfig()
  await loadBackups()
})
</script>
