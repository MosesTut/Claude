from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import auth, preferences, cities, itineraries, feedback, user

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Timbuktoo API",
    description="AI-powered travel planning API for Timbuktoo Mobile MVP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow mobile app to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(preferences.router)
app.include_router(cities.router)
app.include_router(itineraries.router)
app.include_router(feedback.router)
app.include_router(user.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Timbuktoo API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    Used by Datadog, AWS ALB, etc.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
