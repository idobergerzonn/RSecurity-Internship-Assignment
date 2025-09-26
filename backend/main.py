from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from database import db_manager

# Initialize FastAPI app
app = FastAPI(title="Intelligence Reports API", version="1.0.0")

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

# SQLite database storage (replaced dictionary)

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
async def get_reports(tag: Optional[str] = None):
    """
    Get all reports, optionally filtered by tag
    - tag: Optional query parameter to filter by tag
    """
    reports_data = db_manager.get_all_reports(tag)
    return [Report(**report) for report in reports_data]

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Intelligence Reports API is running"}
