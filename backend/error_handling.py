"""
Error handling module for the Intelligence Reports API
Contains all error models, exception handlers, and validation logic
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Optional


# Error response models
class ErrorResponse(BaseModel):
    """Standard error response model"""
    detail: str
    status_code: int


class ValidationErrorDetail(BaseModel):
    """Detailed validation error information"""
    field: str
    message: str
    value: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    """Validation error response model"""
    detail: str
    errors: List[ValidationErrorDetail]
    status_code: int = 422


# Data validation models
class CreateReport(BaseModel):
    """Model for creating a new report with validation"""
    title: str = Field(..., min_length=1, max_length=200, description="Report title")
    content: str = Field(..., min_length=1, description="Report content")
    tags: List[str] = Field(..., min_items=1, description="List of tags")
    
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or contain only whitespace')
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty or contain only whitespace')
        return v.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        if not v:
            raise ValueError('At least one tag is required')
        # Remove empty tags and strip whitespace
        cleaned_tags = [tag.strip() for tag in v if tag.strip()]
        if not cleaned_tags:
            raise ValueError('At least one non-empty tag is required')
        return cleaned_tags


# Exception handlers
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle FastAPI RequestValidationError exceptions
    """
    errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        errors.append(ValidationErrorDetail(
            field=field_path,
            message=error["msg"],
            value=str(error.get("input", "")) if "input" in error else None
        ))
    
    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            detail="Validation error: One or more fields are invalid",
            errors=errors
        ).dict()
    )


async def pydantic_validation_error_handler(request: Request, exc: ValidationError):
    """
    Handle Pydantic ValidationError exceptions
    """
    errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        errors.append(ValidationErrorDetail(
            field=field_path,
            message=error["msg"],
            value=str(error.get("input", "")) if "input" in error else None
        ))
    
    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            detail="Validation error: One or more fields are invalid",
            errors=errors
        ).dict()
    )


async def value_error_handler(request: Request, exc: ValueError):
    """
    Handle custom validation errors from Pydantic validators
    """
    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            detail="Validation error: Invalid field value",
            errors=[ValidationErrorDetail(
                field="body",
                message=str(exc)
            )]
        ).dict()
    )


# Request validation functions
async def validate_request_body(request: Request):
    """
    Validate request body and return appropriate error responses
    Returns tuple: (is_valid, error_response, body_data)
    """
    # Check if request body exists
    body = await request.body()
    if not body:
        return False, JSONResponse(
            status_code=400,
            content=ErrorResponse(
                detail="Request body is required",
                status_code=400
            ).dict()
        ), None
    
    # Parse JSON body
    try:
        import json
        body_data = json.loads(body)
    except json.JSONDecodeError:
        return False, JSONResponse(
            status_code=400,
            content=ErrorResponse(
                detail="Invalid JSON format in request body",
                status_code=400
            ).dict()
        ), None
    
    # Validate that body is not empty object
    if not body_data:
        return False, JSONResponse(
            status_code=400,
            content=ErrorResponse(
                detail="Request body cannot be empty",
                status_code=400
            ).dict()
        ), None
    
    return True, None, body_data


def validate_report_data(body_data):
    """
    Validate report data using Pydantic model
    Returns the validated report model
    """
    try:
        report = CreateReport(**body_data)
        return report
    except ValidationError as e:
        # This will be handled by the ValidationError exception handler
        raise e
    except ValueError as e:
        # This will be handled by the ValueError exception handler
        raise e


def create_error_response(detail: str, status_code: int = 500):
    """
    Generic helper function to create error responses
    """
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            detail=detail,
            status_code=status_code
        ).dict()
    )


def handle_error(error: Exception, context: str = "operation", status_code: int = 500):
    """
    Generic error handler for any operation
    """
    return create_error_response(
        f"Error during {context}: {str(error)}", 
        status_code
    )
