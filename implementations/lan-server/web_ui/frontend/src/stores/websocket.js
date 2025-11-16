import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useWebSocketStore = defineStore('websocket', () => {
  // State
  const connected = ref(false)
  const ws = ref(null)
  const subscriptions = ref(new Set())
  const listeners = ref(new Map())

  // Actions
  function connect(endpoint = '/ws/dashboard') {
    if (ws.value) {
      return // Already connected
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}${endpoint}`

    ws.value = new WebSocket(wsUrl)

    ws.value.onopen = () => {
      connected.value = true
      console.log('WebSocket connected')

      // Resubscribe to events
      if (subscriptions.value.size > 0) {
        send({
          type: 'subscribe',
          events: Array.from(subscriptions.value)
        })
      }
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handleMessage(data)
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err)
      }
    }

    ws.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.value.onclose = () => {
      connected.value = false
      ws.value = null
      console.log('WebSocket disconnected')

      // Auto-reconnect after 5 seconds
      setTimeout(() => {
        if (!connected.value) {
          connect(endpoint)
        }
      }, 5000)
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
      connected.value = false
    }
  }

  function send(data) {
    if (ws.value && connected.value) {
      ws.value.send(JSON.stringify(data))
    }
  }

  function subscribe(eventType, callback) {
    subscriptions.value.add(eventType)

    // Add listener
    if (!listeners.value.has(eventType)) {
      listeners.value.set(eventType, new Set())
    }
    listeners.value.get(eventType).add(callback)

    // Send subscribe message
    if (connected.value) {
      send({
        type: 'subscribe',
        events: [eventType]
      })
    }
  }

  function unsubscribe(eventType, callback) {
    if (callback) {
      const eventListeners = listeners.value.get(eventType)
      if (eventListeners) {
        eventListeners.delete(callback)
        if (eventListeners.size === 0) {
          listeners.value.delete(eventType)
          subscriptions.value.delete(eventType)

          // Send unsubscribe message
          if (connected.value) {
            send({
              type: 'unsubscribe',
              events: [eventType]
            })
          }
        }
      }
    } else {
      listeners.value.delete(eventType)
      subscriptions.value.delete(eventType)

      if (connected.value) {
        send({
          type: 'unsubscribe',
          events: [eventType]
        })
      }
    }
  }

  function handleMessage(data) {
    const eventType = data.type

    // Call all listeners for this event type
    const eventListeners = listeners.value.get(eventType)
    if (eventListeners) {
      eventListeners.forEach(callback => {
        try {
          callback(data)
        } catch (err) {
          console.error('Error in WebSocket listener:', err)
        }
      })
    }

    // Also call global listeners
    const globalListeners = listeners.value.get('*')
    if (globalListeners) {
      globalListeners.forEach(callback => {
        try {
          callback(data)
        } catch (err) {
          console.error('Error in global WebSocket listener:', err)
        }
      })
    }
  }

  return {
    connected,
    connect,
    disconnect,
    send,
    subscribe,
    unsubscribe
  }
})
