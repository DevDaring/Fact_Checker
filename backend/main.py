from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.config.settings import settings
from backend.routes import auth, upload, fact_check, history, admin
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="Fact Checker API",
    description="API for fact-checking multimedia content using Gemini 2.5 Flash with Search Grounding",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(fact_check.router)
app.include_router(history.router)
app.include_router(admin.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Fact Checker API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc)
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("🚀 Fact Checker API is starting...")
    print(f"📁 Data folder: {settings.DATA_FOLDER}")
    print(f"🔑 JWT secret configured: {'Yes' if settings.JWT_SECRET_KEY else 'No'}")
    print(f"🔑 Gemini API configured: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    print(f"🌐 CORS origins: {', '.join(settings.CORS_ORIGINS)}")
    print("✅ API is ready!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    print("👋 Fact Checker API is shutting down...")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=True,
        log_level="info"
    )
