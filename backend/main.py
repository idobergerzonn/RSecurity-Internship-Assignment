from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from database import db_manager

# Initialize FastAPI app
app = FastAPI(title="Intelligence Reports API", version="1.0.0")

# API Key Configuration
API_KEY = "your-secret-api-key-12345"  # Change this to a secure key

# Data models using Pydantic
class Report(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str]
    date: datetime

class CreateReport(BaseModel):
    title: str
    content: str
    tags: List[str]

# API Key Middleware
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    """
    Middleware to check API key for protected endpoints
    """
    # Skip authentication for health check endpoint
    if request.url.path == "/":
        return await call_next(request)
    
    # Check for API key in headers
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "API key required. Please provide X-API-Key header."}
        )
    
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API key."}
        )
    
    # API key is valid, continue with the request
    return await call_next(request)

# API Endpoints
@app.post("/report", response_model=Report)
async def create_report(report: CreateReport):
    """
    Create a new intelligence report
    - title: Report title
    - content: Report content
    - tags: List of tags
    - date: Automatically set to current time
    """
    # Generate unique ID
    report_id = str(uuid.uuid4())
    
    # Create new report
    new_report = Report(
        id=report_id,
        title=report.title,
        content=report.content,
        tags=report.tags,
        date=datetime.now()
    )
    
    # Store in SQLite database
    db_manager.create_report(report_id, report.title, report.content, report.tags, datetime.now())
    
    return new_report

@app.get("/report/{report_id}", response_model=Report)
async def get_report(report_id: str):
    """
    Get a specific report by ID
    """
    report_data = db_manager.get_report(report_id)
    if not report_data:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return Report(**report_data)

@app.get("/reports", response_model=List[Report])
async def get_reports(tag: Optional[str] = None, search: Optional[str] = None):
    """
    Get all reports, optionally filtered by tag and/or search text
    - tag: Optional query parameter to filter by tag
    - search: Optional query parameter to search text in title and content
    """
    reports_data = db_manager.get_reports(search_text=search, tag=tag)
    return [Report(**report) for report in reports_data]

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Intelligence Reports API is running"}
