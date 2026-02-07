"""
UltraViab API - Organ Viability Assessment API
Main application entry point - only responsible for app initialization and route registration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import health_router, prediction_router

app = FastAPI(
    title="UltraViab API",
    description="Organ Viability Assessment API",
    version="1.0.0"
)

# CORS Configuration - Open to all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all controllers/routers
app.include_router(health_router)
app.include_router(prediction_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
