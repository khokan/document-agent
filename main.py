"""
🤖 PDF Knowledge Assistant - RAG Engine

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import router as documents_router
from app.utils import config, logger

# Create FastAPI app
app = FastAPI(
    title=config.app_name,
    description="Local Retrieval-Augmented Generation (RAG) system for PDF document intelligence",
    version=config.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("🚀 Starting PDF Knowledge Assistant...")
    logger.info(f"📚 App: {config.app_name} v{config.app_version}")
    logger.info(f"📂 Upload directory: {config.upload_dir}")
    logger.info(f"💾 ChromaDB collection: {config.chroma_collection_name}")
    logger.info("✅ Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("🛑 Shutting down PDF Knowledge Assistant...")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with application information."""
    return {
        "name": config.app_name,
        "version": config.app_version,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": config.app_name,
        "version": config.app_version,
    }


# Include routers
app.include_router(documents_router)


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "path": str(request.url.path)},
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("🌐 Starting Uvicorn server...")
    uvicorn.run(
        "main:app",
        host=config.get_from_env("APP_HOST", "0.0.0.0"),
        port=int(config.get_from_env("APP_PORT", "8000")),
        reload=config.app_debug,
    )
