import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/client'

export const useDashboardStore = defineStore('dashboard', () => {
  // State
  const stats = ref(null)
  const recentExecutions = ref([])
  const topTools = ref([])
  const executionsByHour = ref({})
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const hasData = computed(() => stats.value !== null)

  // Actions
  async function fetchDashboardData() {
    loading.value = true
    error.value = null

    try {
      const response = await api.getDashboardData()
      stats.value = response.data.stats
      recentExecutions.value = response.data.recent_executions
      topTools.value = response.data.top_tools
      executionsByHour.value = response.data.executions_by_hour
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch dashboard data:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      const response = await api.getSystemStats()
      stats.value = response.data
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  function reset() {
    stats.value = null
    recentExecutions.value = []
    topTools.value = []
    executionsByHour.value = {}
    error.value = null
  }

  return {
    stats,
    recentExecutions,
    topTools,
    executionsByHour,
    loading,
    error,
    hasData,
    fetchDashboardData,
    fetchStats,
    reset
  }
})
