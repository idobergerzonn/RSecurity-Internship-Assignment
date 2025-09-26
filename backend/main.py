from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

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

# In-memory storage (simple dictionary)
reports_db = {}

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
    
    # Store in memory
    reports_db[report_id] = new_report
    
    return new_report

@app.get("/report/{report_id}", response_model=Report)
async def get_report(report_id: str):
    """
    Get a specific report by ID
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return reports_db[report_id]

@app.get("/reports", response_model=List[Report])
async def get_reports(tag: Optional[str] = None):
    """
    Get all reports, optionally filtered by tag
    - tag: Optional query parameter to filter by tag
    """
    all_reports = list(reports_db.values())
    
    if tag:
        # Filter reports that contain the specified tag
        filtered_reports = [report for report in all_reports if tag in report.tags]
        return filtered_reports
    
    return all_reports

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Intelligence Reports API is running"}
