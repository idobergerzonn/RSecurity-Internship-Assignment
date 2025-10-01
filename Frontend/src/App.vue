<script setup>
import { ref, computed, onMounted } from 'vue'
import DataTable from './components/DataTable.vue'
import Charts from './components/Charts.vue'
import SearchFilter from './components/SearchFilter.vue'
import dataService from './services/dataService.js'

// Reactive data
const allData = ref([])
const filteredData = ref([])
const searchTerm = ref('')
const selectedAction = ref('all')
const startDate = ref('')
const endDate = ref('')
const isLoading = ref(true)
const dataLoaded = ref(false)

// Computed properties
const uniqueActions = computed(() => {
  return dataLoaded.value ? dataService.getUniqueActions() : []
})
const actionCounts = computed(() => {
  return dataLoaded.value ? dataService.getActionCounts() : {}
})
const userCounts = computed(() => {
  return dataLoaded.value ? dataService.getUserActivityCounts() : {}
})
const timeData = computed(() => getTimeDistribution())

// Load data on mount
onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  try {
    isLoading.value = true
    await dataService.loadData()
    allData.value = dataService.getAllData()
    dataLoaded.value = true
    applyFilters()
    console.log('Dashboard data loaded:', allData.value.length, 'records')
    console.log('Available actions:', dataService.getUniqueActions())
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    isLoading.value = false
  }
}

const applyFilters = () => {
  let data = dataService.getFilteredData(searchTerm.value, selectedAction.value)
  
  // Apply date filter
  if (startDate.value || endDate.value) {
    data = dataService.filterByDateRange(data, startDate.value, endDate.value)
  }
  
  filteredData.value = data
}


const getTimeDistribution = () => {
  const hourlyData = {}
  
  filteredData.value.forEach(item => {
    const hour = new Date(item.timestamp).getHours()
    hourlyData[hour] = (hourlyData[hour] || 0) + 1
  })
  
  return Object.entries(hourlyData)
    .map(([hour, count]) => ({ hour: `${hour}:00`, count }))
    .sort((a, b) => parseInt(a.hour) - parseInt(b.hour))
}

// Event handlers
const handleSearch = (term) => {
  searchTerm.value = term
  applyFilters()
}

const handleFilter = (action) => {
  selectedAction.value = action
  applyFilters()
}

const handleDateFilter = (dateRange) => {
  startDate.value = dateRange.startDate
  endDate.value = dateRange.endDate
  applyFilters()
}

const handleClearAll = () => {
  searchTerm.value = ''
  selectedAction.value = 'all'
  startDate.value = ''
  endDate.value = ''
  applyFilters()
}
</script>

<template>
  <div class="dashboard-container">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col">
            <h1 class="dashboard-title">
              <i class="bi bi-graph-up me-2"></i>
              Security Dashboard
            </h1>
            <p class="dashboard-subtitle">Monitor and analyze system activity logs</p>
          </div>
          <div class="col-auto">
            <div class="stats-summary">
              <div class="stat-item">
                <span class="stat-number">{{ filteredData.length.toLocaleString() }}</span>
                <span class="stat-label">Total Records</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ uniqueActions.length }}</span>
                <span class="stat-label">Action Types</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container-fluid">
      <!-- Loading State -->
      <div v-if="isLoading" class="loading-container">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading dashboard data...</p>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Search and Filters -->
        <SearchFilter
          :unique-actions="uniqueActions"
          :enable-text-search="true"
          :enable-action-filter="true"
          :enable-date-filter="true"
          @search="handleSearch"
          @filter="handleFilter"
          @date-filter="handleDateFilter"
          @clear-all="handleClearAll"
        />

        <!-- Charts Section -->
        <Charts
          :action-counts="actionCounts"
          :user-counts="userCounts"
          :time-data="timeData"
        />

        <!-- Data Table -->
        <DataTable
          :data="filteredData"
          :total-records="allData.length"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.dashboard-subtitle {
  color: #6c757d;
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
}

.stats-summary {
  display: flex;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin: 2rem 0;
}

.loading-container p {
  color: #6c757d;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .dashboard-title {
    font-size: 2rem;
  }
  
  .stats-summary {
    gap: 1rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}
</style>
