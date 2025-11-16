<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Security Tools</h1>
      <p class="text-gray-500 mt-2">Execute security testing tools</p>
    </div>

    <!-- Tools Grid -->
    <div v-if="toolsStore.hasTools" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="tool in toolsStore.tools"
        :key="tool.name"
        class="card hover:shadow-lg transition-shadow cursor-pointer"
        @click="selectTool(tool)"
      >
        <div class="flex items-start justify-between mb-3">
          <span :class="[
            'badge',
            tool.category === 'network' ? 'badge-info' :
            tool.category === 'code' ? 'badge-success' :
            tool.category === 'threat' ? 'badge-danger' :
            'badge-warning'
          ]">
            {{ tool.category }}
          </span>
        </div>

        <h3 class="text-lg font-bold mb-2">{{ tool.name }}</h3>
        <p class="text-gray-600 text-sm">{{ tool.description }}</p>

        <div class="mt-4 pt-4 border-t">
          <button class="btn-primary w-full">
            Execute Tool
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="toolsStore.loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500">No tools available</p>
    </div>

    <!-- Tool Execution Modal -->
    <div
      v-if="selectedTool"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold">{{ selectedTool.name }}</h2>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <p class="text-gray-600 mb-6">{{ selectedTool.description }}</p>

          <!-- Parameters Form -->
          <form @submit.prevent="executeTool" class="space-y-4">
            <div
              v-for="(schema, paramName) in selectedTool.input_schema.properties"
              :key="paramName"
              class="space-y-2"
            >
              <label class="block text-sm font-medium text-gray-700">
                {{ paramName }}
                <span v-if="isRequired(paramName)" class="text-red-500">*</span>
              </label>

              <!-- String Input -->
              <input
                v-if="schema.type === 'string' && !schema.enum"
                v-model="parameters[paramName]"
                type="text"
                class="input w-full"
                :required="isRequired(paramName)"
                :placeholder="schema.description || ''"
              />

              <!-- Enum Select -->
              <select
                v-else-if="schema.type === 'string' && schema.enum"
                v-model="parameters[paramName]"
                class="input w-full"
                :required="isRequired(paramName)"
              >
                <option value="">Select...</option>
                <option v-for="option in schema.enum" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>

              <!-- Number Input -->
              <input
                v-else-if="schema.type === 'number' || schema.type === 'integer'"
                v-model.number="parameters[paramName]"
                type="number"
                class="input w-full"
                :required="isRequired(paramName)"
              />

              <!-- Boolean Checkbox -->
              <input
                v-else-if="schema.type === 'boolean'"
                v-model="parameters[paramName]"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />

              <p v-if="schema.description" class="text-xs text-gray-500">
                {{ schema.description }}
              </p>
            </div>

            <!-- Example Parameters -->
            <div v-if="selectedTool.examples && selectedTool.examples.length > 0" class="mt-4">
              <p class="text-sm font-medium text-gray-700 mb-2">Examples:</p>
              <div class="space-y-2">
                <button
                  v-for="(example, index) in selectedTool.examples"
                  :key="index"
                  type="button"
                  @click="loadExample(example)"
                  class="btn-secondary text-xs"
                >
                  Load Example {{ index + 1 }}
                </button>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex justify-end space-x-3 pt-4">
              <button type="button" @click="closeModal" class="btn-secondary">
                Cancel
              </button>
              <button
                type="submit"
                class="btn-primary"
                :disabled="executing"
              >
                <span v-if="executing">Executing...</span>
                <span v-else>Execute</span>
              </button>
            </div>
          </form>

          <!-- Execution Result -->
          <div v-if="executionResult" class="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 class="font-bold mb-3">Execution Result</h3>

            <div class="mb-3">
              <span
                :class="[
                  'badge',
                  executionResult.status === 'completed' ? 'badge-success' :
                  executionResult.status === 'running' ? 'badge-info' :
                  executionResult.status === 'failed' ? 'badge-danger' :
                  'badge-warning'
                ]"
              >
                {{ executionResult.status }}
              </span>
              <span v-if="executionResult.duration" class="ml-2 text-sm text-gray-500">
                Duration: {{ executionResult.duration.toFixed(2) }}s
              </span>
            </div>

            <div v-if="executionResult.error" class="p-3 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
              {{ executionResult.error }}
            </div>

            <div v-else-if="executionResult.result" class="bg-white p-3 rounded border overflow-x-auto">
              <pre class="text-sm">{{ JSON.stringify(executionResult.result, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToolsStore } from '@/stores/tools'

const toolsStore = useToolsStore()

const selectedTool = ref(null)
const parameters = ref({})
const executing = ref(false)
const executionResult = ref(null)

function selectTool(tool) {
  selectedTool.value = tool
  parameters.value = {}
  executionResult.value = null

  // Initialize parameters with defaults
  if (tool.input_schema && tool.input_schema.properties) {
    Object.keys(tool.input_schema.properties).forEach(paramName => {
      const schema = tool.input_schema.properties[paramName]
      if (schema.type === 'boolean') {
        parameters.value[paramName] = false
      }
    })
  }
}

function closeModal() {
  selectedTool.value = null
  parameters.value = {}
  executionResult.value = null
  executing.value = false
}

function isRequired(paramName) {
  return selectedTool.value.input_schema.required?.includes(paramName)
}

function loadExample(example) {
  parameters.value = { ...example }
}

async function executeTool() {
  if (!selectedTool.value) return

  executing.value = true
  executionResult.value = null

  try {
    const result = await toolsStore.executeTool(
      selectedTool.value.name,
      parameters.value
    )
    executionResult.value = result
  } catch (error) {
    executionResult.value = {
      status: 'failed',
      error: error.message || 'Execution failed'
    }
  } finally {
    executing.value = false
  }
}

onMounted(async () => {
  await toolsStore.fetchTools()
})
</script>
