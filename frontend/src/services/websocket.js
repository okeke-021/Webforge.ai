import { io } from 'socket.io-client'

export function connectWebSocket(projectId, handlers) {
  const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
  
  const socket = io(wsUrl, {
    withCredentials: true,
    transports: ['websocket', 'polling'],
    query: { projectId }
  })

  socket.on('connect', () => {
    console.log('WebSocket connected')
    socket.emit('join', { projectId })
  })

  socket.on('generation_status', (data) => {
    if (handlers.onStatus) {
      handlers.onStatus(data)
    }
  })

  socket.on('generation_complete', (data) => {
    if (handlers.onComplete) {
      handlers.onComplete(data)
    }
  })

  socket.on('generation_error', (error) => {
    if (handlers.onError) {
      handlers.onError(error)
    }
  })

  socket.on('disconnect', () => {
    console.log('WebSocket disconnected')
  })

  socket.on('error', (error) => {
    console.error('WebSocket error:', error)
    if (handlers.onError) {
      handlers.onError(error)
    }
  })

  return socket
}
