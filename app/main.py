"""Main FastAPI application for CodeReview AI.

This module provides the core REST API endpoints for code review functionality.
It handles both single code snippet reviews and full pull request analysis.
"""

import logging
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from app.services.code_analyzer import CodeAnalyzer
from app.services.pr_reviewer import PullRequestReviewer
from app.utils.logger import setup_logger
from app.config import settings

# Initialize logger with custom configuration
logger = setup_logger(__name__)

# Create FastAPI application instance
app = FastAPI(
    title="CodeReview AI",
    description="AI-powered intelligent code review assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service instances
code_analyzer = CodeAnalyzer()
pr_reviewer = PullRequestReviewer()


class CodeReviewRequest(BaseModel):
    """Request model for code review endpoint."""
    
    code: str = Field(..., description="Source code to review", min_length=1)
    language: str = Field(..., description="Programming language (e.g., python, javascript)")
    context: Optional[str] = Field(None, description="Additional context about the code")
    severity_threshold: Optional[str] = Field("medium", description="Minimum severity level (low, medium, high)")
    
    @validator('language')
    def validate_language(cls, v):
        """Ensure the language is supported."""
        supported = ['python', 'javascript', 'java', 'go', 'rust', 'typescript', 'cpp', 'csharp']
        if v.lower() not in supported:
            raise ValueError(f"Language must be one of: {', '.join(supported)}")
        return v.lower()


class PullRequestReviewRequest(BaseModel):
    """Request model for pull request review endpoint."""
    
    repo_url: str = Field(..., description="GitHub repository URL")
    pr_number: int = Field(..., description="Pull request number", gt=0)
    include_tests: bool = Field(True, description="Whether to review test files")
    max_files: Optional[int] = Field(50, description="Maximum number of files to review", gt=0, le=200)


class ReviewResponse(BaseModel):
    """Response model for code review results."""
    
    status: str
    summary: str
    issues: list
    suggestions: list
    metrics: Dict
    review_id: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Execute tasks on application startup."""
    logger.info("Starting CodeReview AI application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Warm up ML models if needed
    try:
        await code_analyzer.initialize()
        logger.info("Code analyzer initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize code analyzer: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute cleanup tasks on application shutdown."""
    logger.info("Shutting down CodeReview AI application...")
    await code_analyzer.cleanup()


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to CodeReview AI",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "review": "/review",
            "review_pr": "/review-pr"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check if services are responsive
        analyzer_status = await code_analyzer.health_check()
        
        return {
            "status": "healthy",
            "services": {
                "code_analyzer": analyzer_status,
                "pr_reviewer": "operational"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/review", response_model=ReviewResponse)
async def review_code(request: CodeReviewRequest, background_tasks: BackgroundTasks):
    """Analyze and review a code snippet.
    
    This endpoint performs comprehensive code analysis including:
    - Syntax and semantic checks
    - Code quality assessment
    - Security vulnerability detection
    - Performance optimization suggestions
    - Best practices validation
    
    Args:
        request: CodeReviewRequest containing code and metadata
        background_tasks: FastAPI background tasks for async operations
    
    Returns:
        ReviewResponse with detailed analysis results
    """
    logger.info(f"Received code review request for {request.language}")
    
    try:
        # Perform code analysis
        result = await code_analyzer.analyze(
            code=request.code,
            language=request.language,
            context=request.context,
            severity_threshold=request.severity_threshold
        )
        
        # Log analytics in background
        background_tasks.add_task(
            log_review_analytics,
            language=request.language,
            issues_count=len(result.get('issues', []))
        )
        
        logger.info(f"Code review completed with {len(result.get('issues', []))} issues found")
        
        return ReviewResponse(
            status="success",
            summary=result.get('summary', 'Code review completed'),
            issues=result.get('issues', []),
            suggestions=result.get('suggestions', []),
            metrics=result.get('metrics', {}),
            review_id=result.get('review_id')
        )
        
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Code review failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during code review")


@app.post("/review-pr", response_model=ReviewResponse)
async def review_pull_request(request: PullRequestReviewRequest, background_tasks: BackgroundTasks):
    """Review an entire GitHub pull request.
    
    This endpoint fetches and analyzes all changed files in a PR,
    providing comprehensive feedback on code quality, security,
    and best practices across the entire changeset.
    
    Args:
        request: PullRequestReviewRequest with repo URL and PR number
        background_tasks: FastAPI background tasks for async operations
    
    Returns:
        ReviewResponse with aggregated PR analysis
    """
    logger.info(f"Received PR review request: {request.repo_url} PR#{request.pr_number}")
    
    try:
        # Validate and parse repository URL
        if not request.repo_url.startswith('https://github.com/'):
            raise ValueError("Only GitHub repositories are currently supported")
        
        # Perform PR review
        result = await pr_reviewer.review_pull_request(
            repo_url=request.repo_url,
            pr_number=request.pr_number,
            include_tests=request.include_tests,
            max_files=request.max_files
        )
        
        # Schedule background notification tasks
        background_tasks.add_task(
            notify_pr_review_complete,
            repo_url=request.repo_url,
            pr_number=request.pr_number
        )
        
        logger.info(f"PR review completed for {request.repo_url} PR#{request.pr_number}")
        
        return ReviewResponse(
            status="success",
            summary=result.get('summary', 'PR review completed'),
            issues=result.get('issues', []),
            suggestions=result.get('suggestions', []),
            metrics=result.get('metrics', {}),
            review_id=result.get('review_id')
        )
        
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"PR review failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during PR review")


async def log_review_analytics(language: str, issues_count: int):
    """Log review analytics for monitoring and improvement."""
    logger.info(f"Analytics: language={language}, issues={issues_count}")


async def notify_pr_review_complete(repo_url: str, pr_number: int):
    """Send notification when PR review is complete."""
    logger.info(f"PR review notification: {repo_url} PR#{pr_number}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
