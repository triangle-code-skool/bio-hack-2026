"""
Health controller - handles health check endpoints.
Follows Single Responsibility Principle.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint - API health check."""
    return {"message": "UltraViab API is running"}


@router.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "UltraViab API",
        "version": "1.0.0"
    }
