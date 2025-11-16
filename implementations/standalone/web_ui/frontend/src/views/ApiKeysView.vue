<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">API Keys</h1>
        <p class="text-gray-500 mt-2">Manage API keys for MCP server access</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        Create API Key
      </button>
    </div>

    <!-- API Keys List -->
    <div class="card">
      <div v-if="apiKeys.length > 0" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Used
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="key in apiKeys" :key="key.key_id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div>
                  <div class="font-medium text-gray-900">{{ key.name }}</div>
                  <div v-if="key.description" class="text-sm text-gray-500">{{ key.description }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(key.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ key.last_used_at ? formatDate(key.last_used_at) : 'Never' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'badge',
                  key.is_active ? 'badge-success' : 'badge-danger'
                ]">
                  {{ key.is_active ? 'Active' : 'Revoked' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button
                  v-if="key.is_active"
                  @click="revokeKey(key.key_id)"
                  class="text-yellow-600 hover:text-yellow-900"
                >
                  Revoke
                </button>
                <button
                  v-else
                  @click="activateKey(key.key_id)"
                  class="text-green-600 hover:text-green-900"
                >
                  Activate
                </button>
                <button
                  @click="deleteKey(key.key_id)"
                  class="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center py-12">
        <p class="text-gray-500">No API keys found. Create one to get started.</p>
      </div>
    </div>

    <!-- Create API Key Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeCreateModal"
    >
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <h2 class="text-2xl font-bold mb-6">Create API Key</h2>

        <form @submit.prevent="createKey" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Name *
            </label>
            <input
              v-model="newKey.name"
              type="text"
              class="input w-full"
              required
              placeholder="My API Key"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              v-model="newKey.description"
              class="input w-full"
              rows="3"
              placeholder="Optional description"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Permissions
            </label>
            <select
              v-model="newKey.permissions"
              class="input w-full"
              multiple
            >
              <option value="*">All Permissions</option>
              <option value="network_*">Network Tools</option>
              <option value="code_*">Code Analysis</option>
              <option value="threat_*">Threat Intelligence</option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Hold Ctrl/Cmd to select multiple</p>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="closeCreateModal" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary" :disabled="creating">
              {{ creating ? 'Creating...' : 'Create' }}
            </button>
          </div>
        </form>

        <!-- Created Key Display -->
        <div v-if="createdKey" class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded">
          <h3 class="font-bold text-yellow-900 mb-2">⚠️ Save this API key!</h3>
          <p class="text-sm text-yellow-800 mb-3">
            This is the only time you'll see this key. Copy it now.
          </p>
          <div class="flex items-center space-x-2">
            <input
              :value="createdKey"
              type="text"
              class="input flex-1 font-mono text-sm"
              readonly
            />
            <button @click="copyKey" class="btn-secondary">
              Copy
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/client'

const apiKeys = ref([])
const loading = ref(false)
const showCreateModal = ref(false)
const creating = ref(false)
const createdKey = ref('')

const newKey = ref({
  name: '',
  description: '',
  permissions: ['*']
})

async function loadApiKeys() {
  loading.value = true
  try {
    const response = await api.getApiKeys()
    apiKeys.value = response.data
  } catch (error) {
    console.error('Failed to load API keys:', error)
  } finally {
    loading.value = false
  }
}

async function createKey() {
  creating.value = true
  try {
    const response = await api.createApiKey({
      name: newKey.value.name,
      description: newKey.value.description || null,
      permissions: newKey.value.permissions
    })

    createdKey.value = response.data.api_key
    await loadApiKeys()

    // Reset form
    newKey.value = {
      name: '',
      description: '',
      permissions: ['*']
    }
  } catch (error) {
    console.error('Failed to create API key:', error)
    alert('Failed to create API key')
  } finally {
    creating.value = false
  }
}

async function revokeKey(keyId) {
  if (!confirm('Are you sure you want to revoke this API key?')) {
    return
  }

  try {
    await api.revokeApiKey(keyId)
    await loadApiKeys()
  } catch (error) {
    console.error('Failed to revoke API key:', error)
    alert('Failed to revoke API key')
  }
}

async function activateKey(keyId) {
  try {
    await api.activateApiKey(keyId)
    await loadApiKeys()
  } catch (error) {
    console.error('Failed to activate API key:', error)
    alert('Failed to activate API key')
  }
}

async function deleteKey(keyId) {
  if (!confirm('Are you sure you want to delete this API key? This cannot be undone.')) {
    return
  }

  try {
    await api.deleteApiKey(keyId)
    await loadApiKeys()
  } catch (error) {
    console.error('Failed to delete API key:', error)
    alert('Failed to delete API key')
  }
}

function closeCreateModal() {
  showCreateModal.value = false
  createdKey.value = ''
  newKey.value = {
    name: '',
    description: '',
    permissions: ['*']
  }
}

function copyKey() {
  navigator.clipboard.writeText(createdKey.value)
  alert('API key copied to clipboard!')
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}

onMounted(async () => {
  await loadApiKeys()
})
</script>
