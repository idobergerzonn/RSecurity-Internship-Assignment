# Intelligence Reports API

A secure REST API for managing intelligence reports with authentication and search capabilities.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python run_server.py
   ```

3. **Verify server is running:**
   - Open browser and go to `http://localhost:8000`
   - You should see: `{"message": "Intelligence Reports API is running"}`

## API Documentation

### View Interactive Documentation

To view the complete API documentation with interactive testing capabilities:

1. **Go to Swagger Editor**: https://editor.swagger.io/
2. **Click "File" → "Import File"**
3. **Upload the `swagger.yaml` file** from this project
4. **Explore the API** with full interactive documentation

The Swagger documentation includes:
- All available endpoints
- Request/response schemas
- Authentication requirements
- Example requests and responses

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Health check | No |
| POST | `/report` | Create new report | Yes |
| GET | `/report/{id}` | Get specific report | Yes |
| GET | `/reports` | Get all reports (with filters) | Yes |

## Authentication

All endpoints except the health check require an API key:
- **Header**: `X-API-Key`
- **Value**: `your-secret-api-key-12345`

## Features

- Create and manage intelligence reports
- Search reports by content
- Filter reports by tags
- Secure API key authentication
- SQLite database storage
- RESTful API design

## Files

- `main.py` - FastAPI application
- `database.py` - Database management
- `error_handling.py` - Comprehensive error handling, validation models, and exception handlers
- `swagger.yaml` - API documentation
- `requirements.txt` - Python dependencies
- `run_server.py` - Server startup script

