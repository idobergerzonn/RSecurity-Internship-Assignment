<template>
  <div class="search-filter-container">
    <div class="row">
      <!-- Search Input -->
      <div class="col-md-6 mb-3">
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
      <div class="col-md-3 mb-3">
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
      <div class="col-md-3 mb-3">
        <select 
          class="form-select" 
          v-model="selectedDateRange"
          @change="handleDateFilter"
        >
          <option value="all">All Time</option>
          <option value="today">Today</option>
          <option value="yesterday">Yesterday</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
        </select>
      </div>
    </div>

    <!-- Filter Summary -->
    <div v-if="hasActiveFilters" class="filter-summary">
      <div class="d-flex align-items-center flex-wrap gap-2">
        <span class="text-muted">Active filters:</span>
        
        <span v-if="searchTerm" class="badge bg-primary">
          Search: "{{ searchTerm }}"
          <button 
            class="btn-close btn-close-white ms-1" 
            @click="clearSearch"
            style="font-size: 0.7em;"
          ></button>
        </span>
        
        <span v-if="selectedAction !== 'all'" class="badge bg-info">
          Action: {{ formatAction(selectedAction) }}
          <button 
            class="btn-close btn-close-white ms-1" 
            @click="clearActionFilter"
            style="font-size: 0.7em;"
          ></button>
        </span>
        
        <span v-if="selectedDateRange !== 'all'" class="badge bg-warning">
          Date: {{ selectedDateRange }}
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
  }
})

const emit = defineEmits(['search', 'filter', 'dateFilter', 'clearAll'])

const searchTerm = ref('')
const selectedAction = ref('all')
const selectedDateRange = ref('all')

const hasActiveFilters = computed(() => {
  return searchTerm.value || selectedAction.value !== 'all' || selectedDateRange.value !== 'all'
})

const handleSearch = () => {
  emit('search', searchTerm.value)
}

const handleFilter = () => {
  emit('filter', selectedAction.value)
}

const handleDateFilter = () => {
  emit('dateFilter', selectedDateRange.value)
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
  selectedDateRange.value = 'all'
  emit('dateFilter', 'all')
}

const clearAllFilters = () => {
  searchTerm.value = ''
  selectedAction.value = 'all'
  selectedDateRange.value = 'all'
  emit('clearAll')
}

const formatAction = (action) => {
  return action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
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
  padding: 1.5rem;
  margin-bottom: 1.5rem;
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
