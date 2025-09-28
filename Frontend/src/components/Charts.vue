<template>
  <div class="charts-container">
    <!-- Time Series Chart -->
    <div class="row">
      <div class="col-12 mb-4">
        <div class="chart-card">
          <div class="chart-header">
            <h4>Activity Over Time</h4>
            <p class="text-muted">Hourly activity distribution</p>
          </div>
          <div class="chart-wrapper">
            <canvas ref="timeChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Action Counts Bar Chart -->
      <div class="col-lg-6 mb-4">
        <div class="chart-card">
          <div class="chart-header">
            <h4>Action Distribution</h4>
            <p class="text-muted">Number of actions by type</p>
          </div>
          <div class="chart-wrapper">
            <canvas ref="actionChart"></canvas>
          </div>
        </div>
      </div>

      <!-- User Activity Pie Chart -->
      <div class="col-lg-6 mb-4">
        <div class="chart-card">
          <div class="chart-header">
            <h4>Top User Activity</h4>
            <p class="text-muted">Most active users (Top 10)</p>
          </div>
          <div class="chart-wrapper">
            <canvas ref="userChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
  BarController,
  DoughnutController, 
  LineController 
} from 'chart.js'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
  BarController,
  DoughnutController,
  LineController 
)

const props = defineProps({
  actionCounts: {
    type: Object,
    required: true
  },
  userCounts: {
    type: Object,
    required: true
  },
  timeData: {
    type: Array,
    required: true
  }
})

const actionChart = ref(null)
const userChart = ref(null)
const timeChart = ref(null)

let actionChartInstance = null
let userChartInstance = null
let timeChartInstance = null

const createActionChart = () => {
  if (actionChartInstance) {
    actionChartInstance.destroy()
  }

  const ctx = actionChart.value.getContext('2d')
  actionChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(props.actionCounts),
      datasets: [{
        label: 'Action Count',
        data: Object.values(props.actionCounts),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#C9CBCF'
        ],
        borderColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#C9CBCF'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

const createUserChart = () => {
  if (userChartInstance) {
    userChartInstance.destroy()
  }

  // Get top 10 users
  const sortedUsers = Object.entries(props.userCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10)
  
  const ctx = userChart.value.getContext('2d')
  userChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: sortedUsers.map(([user]) => user),
      datasets: [{
        data: sortedUsers.map(([,count]) => count),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  })
}

const createTimeChart = () => {
  if (timeChartInstance) {
    timeChartInstance.destroy()
  }

  const ctx = timeChart.value.getContext('2d')
  timeChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: props.timeData.map(item => item.hour),
      datasets: [{
        label: 'Activity Count',
        data: props.timeData.map(item => item.count),
        borderColor: '#36A2EB',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

onMounted(() => {
  createActionChart()
  createUserChart()
  createTimeChart()
})

// Watch for data changes
watch(() => props.actionCounts, () => {
  createActionChart()
}, { deep: true })

watch(() => props.userCounts, () => {
  createUserChart()
}, { deep: true })

watch(() => props.timeData, () => {
  createTimeChart()
}, { deep: true })
</script>

<style scoped>
.charts-container {
  margin-top: 2rem;
}

.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.chart-header {
  padding: 1.5rem 1.5rem 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.chart-header h4 {
  margin: 0 0 0.5rem 0;
  color: #495057;
}

.chart-header p {
  margin: 0;
  font-size: 0.9rem;
}

.chart-wrapper {
  padding: 1.5rem;
  height: 300px;
  position: relative;
}

@media (max-width: 768px) {
  .chart-wrapper {
    height: 250px;
  }
}
</style>
