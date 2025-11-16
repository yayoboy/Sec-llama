<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">AI Configuration</h1>
      <p class="text-gray-500 mt-2">Configure AI models and providers</p>
    </div>

    <!-- AI Status Card -->
    <div class="card mb-6" :class="aiStatus?.overall_status === 'online' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-bold" :class="aiStatus?.overall_status === 'online' ? 'text-green-900' : 'text-red-900'">
            AI Service Status
          </h3>
          <p class="text-sm mt-1" :class="aiStatus?.overall_status === 'online' ? 'text-green-700' : 'text-red-700'">
            {{ aiStatus?.overall_status === 'online' ? 'Connected and ready' : 'Service unavailable' }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <div v-if="aiStatus?.ollama" class="text-right">
            <p class="text-sm font-medium">Ollama</p>
            <span :class="['badge', aiStatus.ollama.status === 'online' ? 'badge-success' : 'badge-danger']">
              {{ aiStatus.ollama.status }}
            </span>
            <p v-if="aiStatus.ollama.status === 'online'" class="text-xs text-gray-600 mt-1">
              {{ aiStatus.ollama.models_available }} models
            </p>
          </div>
          <button @click="refreshStatus" class="btn-secondary">
            Refresh
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Ollama Configuration -->
      <div class="card">
        <h2 class="text-xl font-bold mb-4">Ollama Configuration</h2>

        <form @submit.prevent="saveOllamaConfig" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Ollama Host *
            </label>
            <input
              v-model="ollamaConfig.host"
              type="text"
              class="input w-full"
              placeholder="http://localhost:11434"
              required
            />
            <p class="text-xs text-gray-500 mt-1">
              URL del server Ollama (locale o remoto)
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Timeout (seconds)
            </label>
            <input
              v-model.number="ollamaConfig.timeout"
              type="number"
              class="input w-full"
              min="10"
              max="600"
            />
          </div>

          <div class="flex items-center">
            <input
              v-model="ollamaConfig.enabled"
              type="checkbox"
              class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <label class="ml-2 text-sm text-gray-700">
              Enable Ollama integration
            </label>
          </div>

          <div class="flex space-x-3">
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Configuration' }}
            </button>
            <button type="button" @click="testConnection" class="btn-secondary" :disabled="testing">
              {{ testing ? 'Testing...' : 'Test Connection' }}
            </button>
          </div>

          <!-- Connection Test Result -->
          <div v-if="testResult" :class="[
            'p-3 rounded text-sm',
            testResult.success ? 'bg-green-50 border border-green-200 text-green-800' : 'bg-red-50 border border-red-200 text-red-800'
          ]">
            <p class="font-medium">{{ testResult.message }}</p>
            <p v-if="testResult.success" class="mt-1">
              Response time: {{ testResult.response_time?.toFixed(2) }}s
              | Models: {{ testResult.models_available }}
              <span v-if="testResult.version"> | Version: {{ testResult.version }}</span>
            </p>
          </div>
        </form>
      </div>

      <!-- Model Management -->
      <div class="card">
        <h2 class="text-xl font-bold mb-4">Installed Models</h2>

        <!-- Add Model -->
        <div class="mb-4 p-3 bg-gray-50 rounded">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Pull New Model
          </label>
          <div class="flex space-x-2">
            <input
              v-model="newModelName"
              type="text"
              class="input flex-1"
              placeholder="llama3.1:8b"
            />
            <button @click="pullModel" class="btn-primary" :disabled="pulling">
              {{ pulling ? 'Pulling...' : 'Pull' }}
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            Esempi: llama3.1:8b, mixtral:8x7b, codellama:13b
          </p>
        </div>

        <!-- Models List -->
        <div v-if="models.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="model in models"
            :key="model.name"
            class="flex items-center justify-between p-3 bg-gray-50 rounded hover:bg-gray-100"
          >
            <div class="flex-1">
              <p class="font-medium">{{ model.name }}</p>
              <div class="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                <span v-if="model.size">{{ formatBytes(model.size) }}</span>
                <span v-if="model.parameter_size">{{ model.parameter_size }}</span>
                <span v-if="model.quantization">{{ model.quantization }}</span>
              </div>
            </div>
            <div class="flex space-x-2">
              <button
                @click="testModelGeneration(model.name)"
                class="btn-secondary text-xs"
                :disabled="generatingModel === model.name"
              >
                Test
              </button>
              <button
                @click="deleteModel(model.name)"
                class="text-red-600 hover:text-red-900 text-xs font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8 text-gray-500">
          No models installed. Pull a model to get started.
        </div>

        <button @click="loadModels" class="btn-secondary w-full mt-4">
          Refresh Models
        </button>
      </div>

      <!-- Default Model Selection -->
      <div class="card">
        <h2 class="text-xl font-bold mb-4">Default Model</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select Default Model
            </label>
            <select v-model="defaultModel" class="input w-full">
              <option value="">Select a model...</option>
              <option v-for="model in models" :key="model.name" :value="model.name">
                {{ model.name }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">
              This model will be used by default for security analysis
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Temperature
            </label>
            <input
              v-model.number="temperature"
              type="range"
              min="0"
              max="2"
              step="0.1"
              class="w-full"
            />
            <p class="text-xs text-gray-500">
              Current: {{ temperature }} (0 = deterministic, 2 = creative)
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Max Tokens
            </label>
            <input
              v-model.number="maxTokens"
              type="number"
              class="input w-full"
              min="128"
              max="8192"
              step="128"
            />
          </div>

          <button @click="saveAISettings" class="btn-primary w-full" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Settings' }}
          </button>
        </div>
      </div>

      <!-- Test Generation Result -->
      <div v-if="generationResult" class="card">
        <h2 class="text-xl font-bold mb-4">Generation Test Result</h2>
        <div :class="[
          'p-4 rounded',
          generationResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        ]">
          <p class="font-medium mb-2">
            {{ generationResult.success ? 'Success!' : 'Failed' }}
          </p>
          <div v-if="generationResult.success" class="space-y-2">
            <div class="bg-white p-3 rounded text-sm">
              {{ generationResult.response }}
            </div>
            <div class="text-xs text-gray-600">
              Duration: {{ generationResult.duration?.toFixed(2) }}s
              | Tokens: {{ generationResult.tokens }}
            </div>
          </div>
          <p v-else class="text-sm text-red-800">
            {{ generationResult.error }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/client'

const aiStatus = ref(null)
const ollamaConfig = ref({
  host: 'http://localhost:11434',
  timeout: 120,
  enabled: true
})
const models = ref([])
const defaultModel = ref('')
const temperature = ref(0.7)
const maxTokens = ref(2048)
const newModelName = ref('')

const saving = ref(false)
const testing = ref(false)
const pulling = ref(false)
const generatingModel = ref(null)

const testResult = ref(null)
const generationResult = ref(null)

async function loadAIConfig() {
  try {
    const response = await api.getAIConfiguration()
    const config = response.data

    ollamaConfig.value = config.ollama
    defaultModel.value = config.default_model
    temperature.value = config.temperature
    maxTokens.value = config.max_tokens
  } catch (error) {
    console.error('Failed to load AI config:', error)
  }
}

async function loadModels() {
  try {
    const response = await api.listAIModels()
    models.value = response.data
  } catch (error) {
    console.error('Failed to load models:', error)
    alert('Failed to load models. Is Ollama running?')
  }
}

async function refreshStatus() {
  try {
    const response = await api.getAIStatus()
    aiStatus.value = response.data
  } catch (error) {
    console.error('Failed to refresh status:', error)
  }
}

async function saveOllamaConfig() {
  saving.value = true
  try {
    await api.updateAIConfiguration({
      ollama: ollamaConfig.value
    })
    alert('Ollama configuration saved!')
    await refreshStatus()
  } catch (error) {
    console.error('Failed to save config:', error)
    alert('Failed to save configuration')
  } finally {
    saving.value = false
  }
}

async function saveAISettings() {
  saving.value = true
  try {
    await api.updateAIConfiguration({
      default_model: defaultModel.value,
      temperature: temperature.value,
      max_tokens: maxTokens.value
    })
    alert('AI settings saved!')
  } catch (error) {
    console.error('Failed to save settings:', error)
    alert('Failed to save settings')
  } finally {
    saving.value = false
  }
}

async function testConnection() {
  testing.value = true
  testResult.value = null

  try {
    const response = await api.testAIConnection(
      ollamaConfig.value.host,
      ollamaConfig.value.timeout
    )
    testResult.value = response.data
  } catch (error) {
    console.error('Connection test failed:', error)
    testResult.value = {
      success: false,
      message: 'Connection test failed'
    }
  } finally {
    testing.value = false
  }
}

async function pullModel() {
  if (!newModelName.value) {
    alert('Please enter a model name')
    return
  }

  pulling.value = true
  try {
    await api.pullAIModel(newModelName.value)
    alert(`Started pulling model: ${newModelName.value}\nThis may take several minutes.`)
    newModelName.value = ''

    // Refresh models after a delay
    setTimeout(loadModels, 5000)
  } catch (error) {
    console.error('Failed to pull model:', error)
    alert('Failed to pull model')
  } finally {
    pulling.value = false
  }
}

async function deleteModel(modelName) {
  if (!confirm(`Are you sure you want to delete model: ${modelName}?`)) {
    return
  }

  try {
    await api.deleteAIModel(modelName)
    await loadModels()
    alert('Model deleted successfully')
  } catch (error) {
    console.error('Failed to delete model:', error)
    alert('Failed to delete model')
  }
}

async function testModelGeneration(modelName) {
  generatingModel.value = modelName
  generationResult.value = null

  try {
    const response = await api.testAIGeneration(modelName, 'Hello, introduce yourself briefly.')
    generationResult.value = response.data
  } catch (error) {
    console.error('Generation test failed:', error)
    generationResult.value = {
      success: false,
      error: 'Generation test failed'
    }
  } finally {
    generatingModel.value = null
  }
}

function formatBytes(bytes) {
  if (!bytes) return 'N/A'
  const gb = bytes / (1024 ** 3)
  return `${gb.toFixed(2)} GB`
}

onMounted(async () => {
  await Promise.all([
    loadAIConfig(),
    loadModels(),
    refreshStatus()
  ])
})
</script>
