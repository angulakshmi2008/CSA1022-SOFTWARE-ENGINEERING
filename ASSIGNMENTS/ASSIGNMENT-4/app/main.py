"""
Smart Campus Facility Platform - Main FastAPI Application.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, engine, get_db
from app.models.user import User
from app.routers import approvals, auth, bookings, facilities, integrations, sensors, tickets
from app.schemas.booking import BookingCreate, BookingResponse
from app.security.authorization import require_authenticated
from app.services.booking_service import BookingService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize tables on startup for local development and test runs
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Smart Campus Facility and Maintenance Platform (CO4 Delivery)",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health & Readiness probe
@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """
    Readiness and liveness probe for container orchestration and release gates.
    Verifies API responsiveness and database connectivity.
    """
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "UP" if db_status == "healthy" else "DEGRADED",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "health_url": "/health",
    }


# Mount v1 API Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(facilities.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(approvals.router, prefix="/api/v1")
app.include_router(sensors.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(integrations.router, prefix="/api/v1")


# Q6: Revised API v2 compatibility endpoint for campus-aware booking
@app.post(
    "/api/v2/bookings",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Bookings v2 (Campus Aware)"],
)
def create_booking_v2(
    booking_in: BookingCreate,
    campus_override: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """
    Revised Booking API v2: Campus policy-aware booking endpoint.
    Maintains backward compatibility with v1 while exposing multi-campus capabilities.
    """
    service = BookingService(db)
    try:
        booking = service.create_booking(booking_in, current_user)
        return booking
    except ValueError as e:
        msg = str(e)
        if "overlaps with existing reservation" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg) from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg) from e
