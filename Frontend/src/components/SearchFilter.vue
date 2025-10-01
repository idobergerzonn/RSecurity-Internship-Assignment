<template>
  <div class="search-filter-container">
    <div class="row g-2 align-items-end">
      <!-- Search Input -->
      <div v-if="enableTextSearch" class="col-xl-4 col-lg-5 col-md-6">
        <div class="search-box">
          <div class="input-group">
            <span class="input-group-text">
              <i class="bi bi-search"></i>
            </span>
            <input
              type="text"
              class="form-control"
              placeholder="Search by user, action, IP, or timestamp..."
              v-model="searchTerm"
              @input="handleSearch"
            />
            <button 
              v-if="searchTerm" 
              class="btn btn-outline-secondary" 
              type="button"
              @click="clearSearch"
            >
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Action Filter -->
      <div v-if="enableActionFilter" class="col-xl-2 col-lg-2 col-md-3 col-sm-6">
        <select 
          class="form-select" 
          v-model="selectedAction"
          @change="handleFilter"
        >
          <option value="all">All Actions</option>
          <option 
            v-for="action in uniqueActions" 
            :key="action" 
            :value="action"
          >
            {{ formatAction(action) }}
          </option>
        </select>
      </div>

      <!-- Date Range Filter -->
      <div v-if="enableDateFilter" class="col-xl-6 col-lg-5 col-md-12">
        <div class="row g-2">
          <div class="col-6">
            <label for="startDate" class="form-label small">Start Date</label>
            <input
              type="date"
              id="startDate"
              class="form-control"
              v-model="startDate"
              @change="handleDateFilter"
            />
          </div>
          <div class="col-6">
            <label for="endDate" class="form-label small">End Date</label>
            <input
              type="date"
              id="endDate"
              class="form-control"
              v-model="endDate"
              @change="handleDateFilter"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Summary -->
    <div v-if="hasActiveFilters" class="filter-summary">
      <div class="d-flex align-items-center flex-wrap gap-2">
        <span class="text-muted">Active filters:</span>
        
        <span v-if="enableTextSearch && searchTerm" class="badge bg-primary">
          Search: "{{ searchTerm }}"
          <button 
            class="btn-close btn-close-white ms-1" 
            @click="clearSearch"
            style="font-size: 0.7em;"
          ></button>
        </span>
        
        <span v-if="enableActionFilter && selectedAction !== 'all'" class="badge bg-info">
          Action: {{ formatAction(selectedAction) }}
          <button 
            class="btn-close btn-close-white ms-1" 
            @click="clearActionFilter"
            style="font-size: 0.7em;"
          ></button>
        </span>
        
        <span v-if="enableDateFilter && (startDate || endDate)" class="badge bg-warning">
          Date: {{ formatDateRange() }}
          <button 
            class="btn-close btn-close-white ms-1" 
            @click="clearDateFilter"
            style="font-size: 0.7em;"
          ></button>
        </span>
        
        <button 
          class="btn btn-sm btn-outline-secondary"
          @click="clearAllFilters"
        >
          Clear All
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  uniqueActions: {
    type: Array,
    required: true
  },
  enableTextSearch: {
    type: Boolean,
    default: true
  },
  enableActionFilter: {
    type: Boolean,
    default: true
  },
  enableDateFilter: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['search', 'filter', 'dateFilter', 'clearAll'])

const searchTerm = ref('')
const selectedAction = ref('all')
const startDate = ref('')
const endDate = ref('')

const hasActiveFilters = computed(() => {
  let hasActive = false
  
  if (props.enableTextSearch && searchTerm.value) {
    hasActive = true
  }
  
  if (props.enableActionFilter && selectedAction.value !== 'all') {
    hasActive = true
  }
  
  if (props.enableDateFilter && (startDate.value || endDate.value)) {
    hasActive = true
  }
  
  return hasActive
})

const handleSearch = () => {
  emit('search', searchTerm.value)
}

const handleFilter = () => {
  emit('filter', selectedAction.value)
}

const handleDateFilter = () => {
  emit('dateFilter', { startDate: startDate.value, endDate: endDate.value })
}

const clearSearch = () => {
  searchTerm.value = ''
  emit('search', '')
}

const clearActionFilter = () => {
  selectedAction.value = 'all'
  emit('filter', 'all')
}

const clearDateFilter = () => {
  startDate.value = ''
  endDate.value = ''
  emit('dateFilter', { startDate: '', endDate: '' })
}

const clearAllFilters = () => {
  if (props.enableTextSearch) {
    searchTerm.value = ''
    emit('search', '')
  }
  
  if (props.enableActionFilter) {
    selectedAction.value = 'all'
    emit('filter', 'all')
  }
  
  if (props.enableDateFilter) {
    startDate.value = ''
    endDate.value = ''
    emit('dateFilter', { startDate: '', endDate: '' })
  }
  
  emit('clearAll')
}

const formatAction = (action) => {
  return action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const formatDateRange = () => {
  if (startDate.value && endDate.value) {
    return `${startDate.value} to ${endDate.value}`
  } else if (startDate.value) {
    return `from ${startDate.value}`
  } else if (endDate.value) {
    return `until ${endDate.value}`
  }
  return ''
}

// Watch for external changes
watch(() => props.uniqueActions, (newActions) => {
  if (selectedAction.value !== 'all' && !newActions.includes(selectedAction.value)) {
    selectedAction.value = 'all'
    emit('filter', 'all')
  }
})
</script>

<style scoped>
.search-filter-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.row.g-2 {
  --bs-gutter-x: 0.75rem;
  --bs-gutter-y: 0.5rem;
}

.align-items-end {
  align-items: flex-end !important;
}

.search-box .input-group-text {
  background: #f8f9fa;
  border-right: none;
}

.search-box .form-control {
  border-left: none;
}

.search-box .form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.filter-summary {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.badge {
  font-size: 0.8rem;
  padding: 0.4rem 0.6rem;
}

.btn-close {
  padding: 0;
  margin: 0;
  background: none;
  border: none;
  opacity: 0.7;
}

.btn-close:hover {
  opacity: 1;
}

.form-select:focus,
.form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}
</style>
