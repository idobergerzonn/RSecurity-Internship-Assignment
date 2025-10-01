from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from datetime import datetime
import uuid
from database import db_manager
from error_handling import (
    ErrorResponse, ValidationErrorResponse,
    validate_request_body, validate_report_data, create_error_response, handle_error,
    validation_exception_handler, pydantic_validation_error_handler, value_error_handler
)

# Initialize FastAPI app
app = FastAPI(title="Intelligence Reports API", version="1.0.0")

# API Key Configuration
API_KEY = "Rsecurity"  # Change this to a secure key

# Data models using Pydantic
class Report(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str]
    date: datetime

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_error_handler)
app.add_exception_handler(ValueError, value_error_handler)


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
@app.post("/report", response_model=Report, responses={
    200: {"description": "Report created successfully"},
    400: {"description": "Bad request - Missing or invalid request body", "model": ErrorResponse},
    422: {"description": "Validation error - Invalid field values", "model": ValidationErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def create_report(request: Request):
    """
    Create a new intelligence report
    - title: Report title (required, 1-200 characters)
    - content: Report content (required, non-empty)
    - tags: List of tags (required, at least one non-empty tag)
    - date: Automatically set to current time
    """
    try:
        # Validate request body
        is_valid, error_response, body_data = await validate_request_body(request)
        if not is_valid:
            return error_response
        
        # Validate report data
        report = validate_report_data(body_data)
        
        # Generate unique ID and create report
        report_id = str(uuid.uuid4())
        new_report = Report(
            id=report_id,
            title=report.title,
            content=report.content,
            tags=report.tags,
            date=datetime.now()
        )
        
        # Store in database
        db_manager.create_report(report_id, report.title, report.content, report.tags, datetime.now())
        return new_report
        
    except (ValidationError, ValueError) as e:
        raise e  # Handled by exception handlers
    except Exception as e:
        return handle_error(e, "creating report")

@app.get("/report/{report_id}", response_model=Report, responses={
    200: {"description": "Report found successfully"},
    404: {"description": "Report not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_report(report_id: str):
    """
    Get a specific report by ID
    - report_id: UUID of the report to retrieve
    """
    try:
        report_data = db_manager.get_report(report_id)
        if not report_data:
            return create_error_response(f"Report with ID '{report_id}' not found", 404)
        
        return Report(**report_data)
    except Exception as e:
        return handle_error(e, "retrieving report")

@app.get("/reports", response_model=List[Report], responses={
    200: {"description": "Reports retrieved successfully"},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_reports(tag: Optional[str] = None, search: Optional[str] = None):
    """
    Get all reports, optionally filtered by tag and/or search text
    - tag: Optional query parameter to filter by tag
    - search: Optional query parameter to search text in title and content
    """
    try:
        reports_data = db_manager.get_reports(search_text=search, tag=tag)
        return [Report(**report) for report in reports_data]
    except Exception as e:
        return handle_error(e, "retrieving reports")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Intelligence Reports API is running"}
