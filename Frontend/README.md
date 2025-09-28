## 📋 Prerequisites

- **Node.js** (version 14 or higher recommended)
- npm (comes with Node.js)

## 🚀 Getting Started

1. Install dependencies: `npm install`
2. Start development server: `npm start`
3. Open http://localhost:5173 in your browser


## ✨ Features

- **Data Visualization** - Bar, doughnut, and line charts
- **Data Table** - Sortable with pagination (20 items/page)
- **Advanced Filtering** - Search, category, and date range filters
- **Responsive Design** - Mobile and desktop optimized
- **Interactive UI** - Hover effects, tooltips, real-time updates

## 📊 Data

Loads 416 security log records from `sample_logs_no_status.json` with fields:
- `timestamp` - Activity time
- `user_id` - User identifier  
- `action` - Action type (login_success, download_file, etc.)
- `ip_address` - Source IP

## 🛠️ Tech Stack

- Vue.js 3 (Composition API)
- Bootstrap 5
- Chart.js
- Vite
