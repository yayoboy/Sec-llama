import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/client'

export const useToolsStore = defineStore('tools', () => {
  // State
  const tools = ref([])
  const categories = ref([])
  const executionHistory = ref([])
  const activeExecution = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const toolsByCategory = computed(() => {
    const grouped = {}
    tools.value.forEach(tool => {
      if (!grouped[tool.category]) {
        grouped[tool.category] = []
      }
      grouped[tool.category].push(tool)
    })
    return grouped
  })

  const hasTools = computed(() => tools.value.length > 0)

  // Actions
  async function fetchTools() {
    loading.value = true
    error.value = null

    try {
      const response = await api.getTools()
      tools.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch tools:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await api.getToolCategories()
      categories.value = response.data
    } catch (err) {
      console.error('Failed to fetch categories:', err)
    }
  }

  async function executeTool(toolName, parameters) {
    loading.value = true
    error.value = null

    try {
      const response = await api.executeTool(toolName, parameters)
      activeExecution.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to execute tool:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchExecutionStatus(executionId) {
    try {
      const response = await api.getExecutionStatus(executionId)
      if (activeExecution.value && activeExecution.value.execution_id === executionId) {
        activeExecution.value = response.data
      }
      return response.data
    } catch (err) {
      console.error('Failed to fetch execution status:', err)
      throw err
    }
  }

  async function fetchExecutionHistory(params = {}) {
    try {
      const response = await api.getExecutionHistory(params)
      executionHistory.value = response.data
    } catch (err) {
      console.error('Failed to fetch execution history:', err)
    }
  }

  function clearActiveExecution() {
    activeExecution.value = null
  }

  function reset() {
    tools.value = []
    categories.value = []
    executionHistory.value = []
    activeExecution.value = null
    error.value = null
  }

  return {
    tools,
    categories,
    executionHistory,
    activeExecution,
    loading,
    error,
    toolsByCategory,
    hasTools,
    fetchTools,
    fetchCategories,
    executeTool,
    fetchExecutionStatus,
    fetchExecutionHistory,
    clearActiveExecution,
    reset
  }
})
