// Data service to load and process JSON data
export class DataService {
  constructor() {
    this.data = []
    this.isLoaded = false
  }

  async loadData() {
    if (this.isLoaded) {
      return this.data
    }

    try {
      const response = await fetch('/sample_logs_no_status.json')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      this.data = await response.json()
      this.isLoaded = true
      console.log('Data loaded successfully:', this.data.length, 'records')
      return this.data
    } catch (error) {
      console.error('Error loading data:', error)
      this.data = []
      return []
    }
  }

  // Get all data
  getAllData() {
    return this.data
  }

  // Get filtered data based on search term
  getFilteredData(searchTerm = '', filterBy = 'all') {
    let filtered = this.data

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(item => 
        item.user_id.toLowerCase().includes(term) ||
        item.action.toLowerCase().includes(term) ||
        item.ip_address.toLowerCase().includes(term) ||
        item.timestamp.toLowerCase().includes(term)
      )
    }

    // Apply category filter
    if (filterBy !== 'all') {
      filtered = filtered.filter(item => item.action === filterBy)
    }

    return filtered
  }
  
  // Filter data by date range
  filterByDateRange(data, startDate, endDate) {
    return data.filter(item => {
      const itemDate = new Date(item.timestamp)
      const itemDateString = itemDate.toISOString().split('T')[0] // Get YYYY-MM-DD format
      
      let startMatch = true
      let endMatch = true
      
      if (startDate) {
        startMatch = itemDateString >= startDate
      }
      
      if (endDate) {
        endMatch = itemDateString <= endDate
      }
      
      return startMatch && endMatch
    })
  }

  // Get unique actions for filter dropdown
  getUniqueActions() {
    const actions = [...new Set(this.data.map(item => item.action))]
    return actions
  }

  // Get action counts for chart
  getActionCounts() {
    const counts = {}
    this.data.forEach(item => {
      counts[item.action] = (counts[item.action] || 0) + 1
    })
    return counts
  }

  // Get user activity counts
  getUserActivityCounts() {
    const counts = {}
    this.data.forEach(item => {
      counts[item.user_id] = (counts[item.user_id] || 0) + 1
    })
    return counts
  }

}

export default new DataService()
