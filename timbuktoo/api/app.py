"""FastAPI application for Timbuktoo multi-tenant API"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid

from ..utils.onboarding import get_onboarding_manager
from ..utils.tenant_manager import get_tenant_manager
from ..security.rbac import get_auth_manager, Permission
from ..utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Timbuktoo Travel Concierge API",
    description="Multi-tenant AI travel planning API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models

class StartOnboardingRequest(BaseModel):
    email: str = Field(..., description="User email")
    tenant_id: Optional[str] = Field(None, description="Existing tenant ID (optional)")


class CompleteSignupRequest(BaseModel):
    session_id: str
    tenant_name: str = Field(..., min_length=3, max_length=63)
    company_name: str
    plan_id: str = Field(default="starter_monthly")


class PreferencesRequest(BaseModel):
    session_id: str
    preferences: Dict[str, Any] = Field(..., description="User travel preferences")


class SelectCityRequest(BaseModel):
    session_id: str
    city_id: str


class FeedbackRequest(BaseModel):
    session_id: str
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None


class UpgradeSubscriptionRequest(BaseModel):
    tenant_id: str
    new_plan_id: str


# Dependency for authentication
async def verify_token(authorization: Optional[str] = Header(None)):
    """Verify JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization[7:]  # Remove "Bearer " prefix

    auth_manager = get_auth_manager()
    payload = auth_manager.verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "timbuktoo-api",
        "version": "1.0.0"
    }


# Onboarding Endpoints

@app.post("/api/v1/onboarding/start")
async def start_onboarding(request: StartOnboardingRequest):
    """
    Start customer onboarding flow

    Step 1: Initialize onboarding session
    """
    onboarding = get_onboarding_manager()
    result = onboarding.start_onboarding(
        email=request.email,
        tenant_id=request.tenant_id
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.post("/api/v1/onboarding/signup")
async def complete_signup(request: CompleteSignupRequest):
    """
    Complete signup step - creates tenant

    Step 2: Tenant signup
    """
    onboarding = get_onboarding_manager()
    result = onboarding.complete_signup(
        session_id=request.session_id,
        tenant_name=request.tenant_name,
        company_name=request.company_name,
        plan_id=request.plan_id
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.post("/api/v1/onboarding/preferences")
async def capture_preferences(request: PreferencesRequest):
    """
    Capture user travel preferences

    Step 3: Preference capture
    """
    onboarding = get_onboarding_manager()
    result = onboarding.capture_preferences(
        session_id=request.session_id,
        preferences=request.preferences
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.post("/api/v1/onboarding/recommend-cities")
async def recommend_cities(session_id: str):
    """
    Get city recommendations

    Step 4: City recommendation
    """
    onboarding = get_onboarding_manager()
    result = onboarding.recommend_cities(session_id=session_id)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.post("/api/v1/onboarding/select-city")
async def select_city(request: SelectCityRequest):
    """
    Select a city

    Step 5: City selection
    """
    onboarding = get_onboarding_manager()
    result = onboarding.select_city(
        session_id=request.session_id,
        city_id=request.city_id
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.post("/api/v1/onboarding/generate-itinerary")
async def generate_itinerary(session_id: str):
    """
    Generate full itinerary

    Step 6: Itinerary delivery
    """
    onboarding = get_onboarding_manager()
    result = onboarding.generate_itinerary(session_id=session_id)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.post("/api/v1/onboarding/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit onboarding feedback

    Step 7: Feedback loop
    """
    onboarding = get_onboarding_manager()
    result = onboarding.collect_feedback(
        session_id=request.session_id,
        rating=request.rating,
        comments=request.comments
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@app.get("/api/v1/onboarding/session/{session_id}")
async def get_onboarding_session(session_id: str):
    """Get onboarding session details"""
    onboarding = get_onboarding_manager()
    result = onboarding.get_session(session_id)

    if not result:
        raise HTTPException(status_code=404, detail="Session not found")

    return result


# Tenant Management Endpoints

@app.get("/api/v1/tenants/{tenant_id}")
async def get_tenant(tenant_id: str, user: dict = Depends(verify_token)):
    """Get tenant details (requires authentication)"""
    tenant_manager = get_tenant_manager()
    result = tenant_manager.get_tenant(tenant_id)

    if not result:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return result


@app.get("/api/v1/tenants/{tenant_id}/quota/{resource_type}")
async def check_quota(tenant_id: str, resource_type: str, user: dict = Depends(verify_token)):
    """Check tenant quota for a resource"""
    tenant_manager = get_tenant_manager()
    result = tenant_manager.check_quota(tenant_id, resource_type)

    return result


@app.post("/api/v1/tenants/{tenant_id}/upgrade")
async def upgrade_subscription(
    tenant_id: str,
    request: UpgradeSubscriptionRequest,
    user: dict = Depends(verify_token)
):
    """Upgrade tenant subscription (requires authentication)"""

    # Check permission
    auth_manager = get_auth_manager()
    if not auth_manager.has_permission(user.get("role"), Permission.MANAGE_USERS):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    tenant_manager = get_tenant_manager()
    result = tenant_manager.upgrade_subscription(tenant_id, request.new_plan_id)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


# Pricing Plans Endpoints

@app.get("/api/v1/plans")
async def list_pricing_plans():
    """List all available pricing plans"""
    from ..database.models import PricingPlan, SessionLocal

    db = SessionLocal()
    try:
        plans = db.query(PricingPlan).filter(PricingPlan.is_active == True).all()
        return [plan.to_dict() for plan in plans]
    finally:
        db.close()


@app.get("/api/v1/plans/{plan_id}")
async def get_pricing_plan(plan_id: str):
    """Get details for a specific pricing plan"""
    from ..database.models import PricingPlan, SessionLocal

    db = SessionLocal()
    try:
        plan = db.query(PricingPlan).filter(PricingPlan.plan_id == plan_id).first()

        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        return plan.to_dict()
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
