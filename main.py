"""
🤖 PDF Knowledge Assistant - RAG Engine

Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import router as documents_router
from app.api.search import router as search_router
from app.api.rag import router as rag_router
from app.utils import config, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle FastAPI lifespan events (startup and shutdown).
    
    This replaces the deprecated @app.on_event() decorators.
    """
    # Startup
    logger.info("[START] Starting PDF Knowledge Assistant...")
    logger.info(f"[INFO] App: {config.app_name} v{config.app_version}")
    logger.info(f"[INFO] Upload directory: {config.upload_dir}")
    logger.info(f"[INFO] ChromaDB collection: {config.chroma_collection_name}")
    logger.info(f"[INFO] RAG Ranker strategy: {config.rag_ranker_strategy}")
    logger.info(f"[INFO] RAG Cache enabled: {config.rag_cache_enabled}")
    logger.info(f"[INFO] RAG Generator model: {config.rag_generator_model}")
    logger.info(f"[INFO] RAG Generator timeout: {config.rag_generator_timeout_seconds}s")
    logger.info("[OK] Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("[STOP] Shutting down PDF Knowledge Assistant...")


# Create FastAPI app with lifespan
app = FastAPI(
    title=config.app_name,
    description="Local Retrieval-Augmented Generation (RAG) system for PDF document intelligence",
    version=config.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(search_router)
app.include_router(rag_router)


if __name__ == "__main__":
    import uvicorn

    logger.info("[SERVER] Starting Uvicorn server...")
    host = config.get_from_env("APP_HOST", "0.0.0.0")
    port = int(config.get_from_env("APP_PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=config.app_debug,
        log_level="info",
    )
