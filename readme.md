# RSecurity Internship Assignment

This repository contains the full solution for the RSecurity Internship Assignment, including all three parts:

- **Frontend:** Interactive dashboard built with Vue.js
- **Backend:** REST API service using FastAPI and SQLite
- **Security/Analysis:** Log analysis script detecting suspicious activity

## How to Run

### Backend
See `backend/README.md` for instructions on running the API (including Docker).

### Frontend
See `frontend/README.md` for instructions on running the dashboard locally.

### Security/Analysis
See `security/README.md` for instructions on analyzing the log files.

## Notes / Assumptions
- Backend runs on port 8000
- Frontend runs on port 5173
- Sample data displayed in the frontend is derived from Part 3 (Security/Analysis)
- SQLite database used for persistence

## Highlights / Extra Features
- Completed all required tasks and all bonus features
- Dockerized backend
- Full Swagger documentation for the API
- API authentication via X-API-Key header
- Search reports by text content
- Responsive frontend design with filtering, charts, and interactive elements (hover tooltips, sorting)
- Nice, clean UI design for the frontend
- Visualizations of anomalies (charts/graphs) in the security analysis
- Suggested mitigations for detected anomalies
- Use of ML-based methods for anomaly detection

