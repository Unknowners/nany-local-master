"""
FastAPI Main Application
Modular structure with routers and services
"""
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Any
import logging
from datetime import datetime

# Import routers
from .routers import onboarding, auth, dev
from .database import get_db, create_tables

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Nanny Match FastAPI", version="0.2.0")

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📥 {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"📤 {request.method} {request.url} → {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"❌ {request.method} {request.url} → Error: {str(e)}")
        raise

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(onboarding.router)
app.include_router(dev.router)

# ===== Basic Endpoints =====

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Nanny Match FastAPI",
        "version": "0.2.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat()
    }

# ===== Generic Table Endpoint =====

@app.get("/api/v1/{table_name}")
async def list_rows(
    table_name: str,
    db: Session = Depends(get_db),
    select: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    order_by: Optional[str] = None,
    **filters: Any
):
    """Generic endpoint for table operations (fallback for unmapped tables)"""
    # Import models here to avoid circular imports
    from .models import (
        Profile, UserRole, ProfilePhoto, Nanny, NannyService, NannyEducation, 
        NannyLanguage, NannyAgeExperience, Certificate, SavedParent, Parent, 
        ParentChild, ParentRequirement, SavedNanny, Booking, Review
    )
    
    # Map table names to models
    table_map = {
        "profiles": Profile,
        "user_roles": UserRole,
        "profile_photos": ProfilePhoto,
        "nannies": Nanny,
        "nanny_services": NannyService,
        "nanny_education": NannyEducation,
        "nanny_languages": NannyLanguage,
        "nanny_age_experience": NannyAgeExperience,
        "certificates": Certificate,
        "saved_parents": SavedParent,
        "parents": Parent,
        "parent_children": ParentChild,
        "parent_requirements": ParentRequirement,
        "saved_nannies": SavedNanny,
        "bookings": Booking,
        "reviews": Review,
    }
    
    if table_name not in table_map:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
    
    model = table_map[table_name]
    query = db.query(model)
    
    # Apply filters
    for key, value in filters.items():
        if "__" in key:
            column, operator = key.split("__", 1)
            if hasattr(model, column):
                if operator == "eq":
                    query = query.filter(getattr(model, column) == value)
                elif operator == "in":
                    if isinstance(value, str):
                        values = value.split(",")
                    else:
                        values = value
                    query = query.filter(getattr(model, column).in_(values))
    
    # Apply ordering
    if order_by:
        parts = order_by.split(":")
        column = parts[0]
        direction = parts[1] if len(parts) > 1 else "asc"
        
        if hasattr(model, column):
            order_column = getattr(model, column)
            if direction == "desc":
                order_column = order_column.desc()
            query = query.order_by(order_column)
    
    # Apply limit
    query = query.limit(limit)
    
    # Execute query
    results = query.all()
    
    # Convert to dict
    data = []
    for item in results:
        item_dict = {}
        for column in item.__table__.columns:
            value = getattr(item, column.name)
            if hasattr(value, 'isoformat'):  # datetime objects
                value = value.isoformat()
            item_dict[column.name] = value
        data.append(item_dict)
    
    return data

# ===== Error Handlers =====

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# ===== Startup Events =====

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("🚀 Starting Nanny Match FastAPI application...")
    
    # Create database tables
    try:
        create_tables()
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {str(e)}")
    
    logger.info("✅ Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("🛑 Shutting down Nanny Match FastAPI application...")
    logger.info("✅ Application shutdown complete")