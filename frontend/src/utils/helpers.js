/**
 * Utility Helper Functions
 */

/**
 * Format date to human-readable string
 */
export const formatDate = (dateString, options = {}) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  // Relative time for recent dates
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  if (days < 30) return `${Math.floor(days / 7)} weeks ago`
  
  // Absolute date for older dates
  const defaultOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options
  }
  
  return date.toLocaleDateString('en-US', defaultOptions)
}

/**
 * Format time to human-readable string
 */
export const formatTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

/**
 * Format file size in bytes to human-readable format
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Truncate string to specified length
 */
export const truncate = (str, length = 50, suffix = '...') => {
  if (str.length <= length) return str
  return str.substring(0, length - suffix.length) + suffix
}

/**
 * Debounce function calls
 */
export const debounce = (func, wait = 300) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * Deep clone object
 */
export const deepClone = (obj) => {
  return JSON.parse(JSON.stringify(obj))
}

/**
 * Generate random ID
 */
export const generateId = () => {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

/**
 * Validate email address
 */
export const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

/**
 * Validate URL
 */
export const isValidUrl = (url) => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Get file extension from filename
 */
export const getFileExtension = (filename) => {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2)
}

/**
 * Get file icon emoji based on extension
 */
export const getFileIcon = (filename) => {
  const ext = getFileExtension(filename).toLowerCase()
  
  const iconMap = {
    // Programming
    'js': '📜',
    'jsx': '⚛️',
    'ts': '📘',
    'tsx': '⚛️',
    'py': '🐍',
    'vue': '💚',
    'java': '☕',
    'go': '🐹',
    'rb': '💎',
    'php': '🐘',
    'swift': '🦅',
    'kt': '🅺',
    
    // Web
    'html': '🌐',
    'css': '🎨',
    'scss': '🎨',
    'sass': '🎨',
    
    // Data
    'json': '📋',
    'xml': '📋',
    'yaml': '📋',
    'yml': '📋',
    'sql': '🗄️',
    
    // Documents
    'md': '📝',
    'txt': '📄',
    'pdf': '📕',
    'doc': '📘',
    'docx': '📘',
    
    // Images
    'jpg': '🖼️',
    'jpeg': '🖼️',
    'png': '🖼️',
    'gif': '🖼️',
    'svg': '🎨',
    
    // Archives
    'zip': '📦',
    'tar': '📦',
    'gz': '📦',
    
    // Config
    'env': '⚙️',
    'config': '⚙️',
    'ini': '⚙️'
  }
  
  return iconMap[ext] || '📄'
}

/**
 * Capitalize first letter of string
 */
export const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

/**
 * Convert camelCase to Title Case
 */
export const camelToTitle = (str) => {
  const result = str.replace(/([A-Z])/g, ' $1')
  return result.charAt(0).toUpperCase() + result.slice(1)
}

/**
 * Convert string to kebab-case
 */
export const toKebabCase = (str) => {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase()
}

/**
 * Get severity color class
 */
export const getSeverityClass = (severity) => {
  const classes = {
    critical: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    low: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    info: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
  }
  return classes[severity] || classes.info
}

/**
 * Get status color class
 */
export const getStatusClass = (status) => {
  const classes = {
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    failed: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    generating: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    analyzing: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400'
  }
  return classes[status] || classes.pending
}

/**
 * Copy text to clipboard
 */
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (err) {
    console.error('Failed to copy:', err)
    return false
  }
}

/**
 * Download file from blob
 */
export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

/**
 * Sleep/delay function
 */
export const sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Parse query string to object
 */
export const parseQueryString = (queryString) => {
  const params = new URLSearchParams(queryString)
  const result = {}
  for (const [key, value] of params) {
    result[key] = value
  }
  return result
}

/**
 * Build query string from object
 */
export const buildQueryString = (params) => {
  return new URLSearchParams(params).toString()
}

/**
 * Check if object is empty
 */
export const isEmpty = (obj) => {
  return Object.keys(obj).length === 0
}

/**
 * Remove null/undefined values from object
 */
export const removeEmpty = (obj) => {
  return Object.fromEntries(
    Object.entries(obj).filter(([_, v]) => v != null)
  )
}

/**
 * Group array of objects by key
 */
export const groupBy = (array, key) => {
  return array.reduce((result, item) => {
    const group = item[key]
    if (!result[group]) {
      result[group] = []
    }
    result[group].push(item)
    return result
  }, {})
}

/**
 * Sort array of objects by key
 */
export const sortBy = (array, key, order = 'asc') => {
  return [...array].sort((a, b) => {
    const aVal = a[key]
    const bVal = b[key]
    
    if (aVal < bVal) return order === 'asc' ? -1 : 1
    if (aVal > bVal) return order === 'asc' ? 1 : -1
    return 0
  })
}

/**
 * Get unique values from array
 */
export const unique = (array) => {
  return [...new Set(array)]
}

/**
 * Chunk array into smaller arrays
 */
export const chunk = (array, size) => {
  const chunks = []
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size))
  }
  return chunks
}

/**
 * Calculate percentage
 */
export const percentage = (value, total) => {
  if (total === 0) return 0
  return Math.round((value / total) * 100)
}

/**
 * Clamp number between min and max
 */
export const clamp = (num, min, max) => {
  return Math.min(Math.max(num, min), max)
}

/**
 * Generate color from string (for avatars, etc)
 */
export const stringToColor = (str) => {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  const color = Math.floor(Math.abs((Math.sin(hash) * 10000) % 1) * 16777215).toString(16)
  return '#' + '0'.repeat(6 - color.length) + color
}

/**
 * Get initials from name
 */
export const getInitials = (name) => {
  if (!name) return '?'
  
  const parts = name.trim().split(' ')
  if (parts.length === 1) {
    return parts[0].substring(0, 2).toUpperCase()
  }
  
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

/**
 * Format duration in seconds to human readable
 */
export const formatDuration = (seconds) => {
  if (seconds < 60) return `${Math.floor(seconds)}s`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`
}

export default {
  formatDate,
  formatTime,
  formatFileSize,
  truncate,
  debounce,
  deepClone,
  generateId,
  isValidEmail,
  isValidUrl,
  getFileExtension,
  getFileIcon,
  capitalize,
  camelToTitle,
  toKebabCase,
  getSeverityClass,
  getStatusClass,
  copyToClipboard,
  downloadBlob,
  sleep,
  parseQueryString,
  buildQueryString,
  isEmpty,
  removeEmpty,
  groupBy,
  sortBy,
  unique,
  chunk,
  percentage,
  clamp,
  stringToColor,
  getInitials,
  formatDuration
}
