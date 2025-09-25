<template>
  <div class="data-table-container">
    <div class="table-header">
      <h3>Activity Logs</h3>
      <div class="table-info">
        Showing {{ paginatedData.length }} of {{ filteredData.length }} records
      </div>
    </div>
    
    <div class="table-responsive">
      <table class="table table-striped table-hover" :key="`table-${currentPage}`">
        <thead class="table-dark">
          <tr>
            <th @click="sortBy('timestamp')" class="sortable" title="Click to sort by timestamp">
              Timestamp 
              <i :class="getSortIcon('timestamp')"></i>
            </th>
            <th @click="sortBy('user_id')" class="sortable" title="Click to sort by user ID">
              User ID 
              <i :class="getSortIcon('user_id')"></i>
            </th>
            <th @click="sortBy('action')" class="sortable" title="Click to sort by action">
              Action 
              <i :class="getSortIcon('action')"></i>
            </th>
            <th @click="sortBy('ip_address')" class="sortable" title="Click to sort by IP address">
              IP Address 
              <i :class="getSortIcon('ip_address')"></i>
            </th>
          </tr>
        </thead>
        <tbody>
            <tr v-for="(item, index) in paginatedData" :key="`page-${currentPage}-${index}-${item.user_id}`" class="table-row">

            <td>{{ formatTimestamp(item.timestamp) }}</td>
            <td>
              <span class="badge bg-primary">{{ item.user_id }}</span>
            </td>
            <td>
              <span :class="getActionBadgeClass(item.action)">
                {{ formatAction(item.action) }}
              </span>
            </td>
            <td>
              <code>{{ item.ip_address }}</code>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination-container">
      <nav class="pagination-nav">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
              Previous
            </button>
          </li>
          
          <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: page === currentPage }">
            <button class="page-link" @click="goToPage(page)">
              {{ page }}
            </button>
          </li>
          
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { computed, ref , watch } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  totalRecords: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['sort'])

const currentPage = ref(1)
const itemsPerPage = 20
const sortField = ref('')
const sortDirection = ref('')

const filteredData = computed(() => {
  // If no sorting is applied, return data in original order
  if (!sortField.value) {
    return [...props.data]
  }
  
  // Apply sorting only when user clicks on a column header
  return [...props.data].sort((a, b) => {
    const aVal = a[sortField.value]
    const bVal = b[sortField.value]
    
    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
})

const totalPages = computed(() => {
  const pages = Math.ceil(filteredData.value.length / itemsPerPage)
  console.log('totalPages computed:', { 
    filteredDataLength: filteredData.value.length, 
    itemsPerPage, 
    totalPages: pages 
  })
  return pages
})





const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  const result = filteredData.value.slice(start, end)
  console.log('paginatedData computed:', { 
    currentPage: currentPage.value, 
    start, 
    end, 
    totalItems: filteredData.value.length, 
    resultLength: result.length,
    result: result
  })
  return result
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
  currentPage.value = 1
  emit('sort', { field, direction: sortDirection.value })
}

const getSortIcon = (field) => {
  if (sortField.value !== field) return 'bi bi-arrow-down-up'
  return sortDirection.value === 'asc' ? 'bi bi-arrow-up' : 'bi bi-arrow-down'
}

const goToPage = (page) => {
  console.log('goToPage called:', { 
    requestedPage: page, 
    currentPage: currentPage.value, 
    totalPages: totalPages.value, 
    isValid: page >= 1 && page <= totalPages.value 
  })
  
  if (page >= 1 && page <= totalPages.value) {
    console.log('Page changed to:', page)
    currentPage.value = page

    console.log('currentPage:', currentPage.value)
    console.log('paginatedData length:', paginatedData.value.length)
  } else {
    console.log('Invalid page number:', page)
  }
}

// Force table update when currentPage changes
watch(currentPage, (newPage, oldPage) => {
  console.log('currentPage watcher triggered:', { newPage, oldPage })
  // Force reactivity by accessing the computed property
  const data = paginatedData.value
  console.log('Forced paginatedData access:', data.length, 'items')
})

const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

const formatAction = (action) => {
  return action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getActionBadgeClass = (action) => {
  const classes = {
    'login_success': 'badge bg-success',
    'login_failed': 'badge bg-danger',
    'download_file': 'badge bg-info',
    'view_report': 'badge bg-warning',
    'change_settings': 'badge bg-secondary'
  }
  return classes[action] || 'badge bg-light text-dark'
}
</script>

<style scoped>
.data-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.table-header h3 {
  margin: 0;
  color: #495057;
}

.table-info {
  color: #6c757d;
  font-size: 0.9rem;
}

.sortable {
  cursor: pointer;
  user-select: none;
  position: relative;
}

.sortable:hover {
  background-color: rgba(0,0,0,0.05);
}

.sortable i {
  margin-left: 0.5rem;
  opacity: 0.7;
}

.table-row:hover {
  background-color: rgba(0,123,255,0.1);
}

.pagination-container {
  margin-top: 1rem;
}

.pagination-nav {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0 0 8px 8px;
}

.pagination {
  margin: 0;
}

.page-link {
  color: #0d6efd;
  text-decoration: none;
  border: 1px solid #dee2e6;
  padding: 0.5rem 0.75rem;
  margin: 0 2px;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
}

.page-link:hover {
  color: #0a58ca;
  background-color: #e9ecef;
  border-color: #dee2e6;
}

.page-item.active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
}

.page-item.disabled .page-link {
  color: #6c757d;
  background-color: #fff;
  border-color: #dee2e6;
  cursor: not-allowed;
}

code {
  background: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.85rem;
}

.table-responsive {
  max-height: 600px;
  overflow-y: auto;
}
</style>