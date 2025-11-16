import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  config => {
    // Add API key if available
    const apiKey = localStorage.getItem('api_key')
    if (apiKey) {
      config.headers['X-API-Key'] = apiKey
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Handle error responses
      console.error('API Error:', error.response.data)
    }
    return Promise.reject(error)
  }
)

export default {
  // Dashboard
  getDashboardData() {
    return apiClient.get('/dashboard')
  },
  getSystemStats() {
    return apiClient.get('/dashboard/stats')
  },
  getRecentExecutions(limit = 10) {
    return apiClient.get('/dashboard/recent-executions', { params: { limit } })
  },

  // Tools
  getTools() {
    return apiClient.get('/tools')
  },
  getToolInfo(toolName) {
    return apiClient.get(`/tools/${toolName}`)
  },
  executeTool(toolName, parameters) {
    return apiClient.post(`/tools/${toolName}/execute`, {
      tool_name: toolName,
      parameters
    })
  },
  getExecutionStatus(executionId) {
    return apiClient.get(`/tools/executions/${executionId}`)
  },
  getExecutionHistory(params = {}) {
    return apiClient.get('/tools/history', { params })
  },
  getToolCategories() {
    return apiClient.get('/tools/categories')
  },

  // Configuration
  getConfiguration() {
    return apiClient.get('/config')
  },
  updateConfiguration(configData, backup = true) {
    return apiClient.put('/config', {
      config_data: configData,
      backup
    })
  },
  validateConfiguration(configData) {
    return apiClient.post('/config/validate', configData)
  },
  createBackup() {
    return apiClient.post('/config/backup')
  },
  listBackups() {
    return apiClient.get('/config/backups')
  },
  restoreBackup(backupId) {
    return apiClient.post(`/config/restore/${backupId}`)
  },
  downloadConfiguration() {
    return apiClient.get('/config/download', {
      responseType: 'blob'
    })
  },
  getConfigurationSchema() {
    return apiClient.get('/config/schema')
  },

  // API Keys
  getApiKeys() {
    return apiClient.get('/api-keys')
  },
  createApiKey(data) {
    return apiClient.post('/api-keys', data)
  },
  getApiKey(keyId) {
    return apiClient.get(`/api-keys/${keyId}`)
  },
  updateApiKey(keyId, data) {
    return apiClient.patch(`/api-keys/${keyId}`, data)
  },
  deleteApiKey(keyId) {
    return apiClient.delete(`/api-keys/${keyId}`)
  },
  revokeApiKey(keyId) {
    return apiClient.post(`/api-keys/${keyId}/revoke`)
  },
  activateApiKey(keyId) {
    return apiClient.post(`/api-keys/${keyId}/activate`)
  },
  getApiKeyUsage(keyId) {
    return apiClient.get(`/api-keys/${keyId}/usage`)
  },

  // Audit Logs
  getAuditLogs(params = {}) {
    return apiClient.get('/audit-logs', { params })
  },
  getAuditLogStats(days = 7) {
    return apiClient.get('/audit-logs/stats', { params: { days } })
  },
  exportAuditLogs(format = 'json', days = 30) {
    return apiClient.get('/audit-logs/export', {
      params: { format, days }
    })
  },
  clearAuditLogs(days = null) {
    return apiClient.delete('/audit-logs', {
      params: days ? { days } : {}
    })
  },

  // AI Configuration
  getAIConfiguration() {
    return apiClient.get('/ai')
  },
  updateAIConfiguration(data) {
    return apiClient.put('/ai', data)
  },
  listAIModels() {
    return apiClient.get('/ai/models')
  },
  pullAIModel(modelName, insecure = false) {
    return apiClient.post('/ai/models/pull', {
      model_name: modelName,
      insecure
    })
  },
  deleteAIModel(modelName) {
    return apiClient.delete(`/ai/models/${modelName}`)
  },
  getAIModelInfo(modelName) {
    return apiClient.get(`/ai/models/${modelName}/info`)
  },
  testAIConnection(host, timeout = 10) {
    return apiClient.post('/ai/test-connection', { host, timeout })
  },
  testAIGeneration(model, prompt = 'Hello!', maxTokens = 50) {
    return apiClient.post('/ai/test-generation', {
      model,
      prompt,
      max_tokens: maxTokens
    })
  },
  getAIStatus() {
    return apiClient.get('/ai/status')
  }
}
