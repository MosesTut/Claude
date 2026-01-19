"""
Timbuktoo Mobile API Endpoints

These endpoints extend the existing Timbuktoo API with mobile-specific functionality.
All endpoints require JWT authentication unless otherwise specified.

Base URL: https://api.timbuktoo.ai
API Version: v1
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import bcrypt
import jwt
import datetime

router = APIRouter(prefix="/api/v1", tags=["mobile"])
security = HTTPBearer()

# ============================================================================
# Authentication Endpoints
# ============================================================================

class SignupRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars, validated client-side

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str
    userId: str
    email: str

@router.post("/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def mobile_signup(request: SignupRequest):
    """
    Mobile-specific signup endpoint.

    Requirements:
    - Email validation
    - Password hashing (bcrypt)
    - JWT token generation (exp: 30 days)
    - Create user in PostgreSQL

    Returns:
    - JWT token (store in SecureStore)
    - User ID
    - Email
    """
    # Check if email already exists
    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    password_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())

    # Create user
    user_id = str(uuid.uuid4())
    await db.users.insert_one({
        "user_id": user_id,
        "email": request.email,
        "password_hash": password_hash,
        "created_at": datetime.datetime.utcnow(),
        "platform": "mobile",
        "ai_consent_given": True,  # Required from onboarding
    })

    # Generate JWT token
    token = jwt.encode({
        "user_id": user_id,
        "email": request.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }, JWT_SECRET, algorithm="HS256")

    return AuthResponse(token=token, userId=user_id, email=request.email)


@router.post("/auth/login", response_model=AuthResponse)
async def mobile_login(request: LoginRequest):
    """
    Mobile-specific login endpoint.

    Requirements:
    - Email/password validation
    - JWT token generation (exp: 30 days)

    Returns:
    - JWT token (store in SecureStore)
    - User ID
    - Email
    """
    # Find user
    user = await db.users.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not bcrypt.checkpw(request.password.encode('utf-8'), user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = jwt.encode({
        "user_id": user["user_id"],
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }, JWT_SECRET, algorithm="HS256")

    return AuthResponse(token=token, userId=user["user_id"], email=user["email"])


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def mobile_logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Mobile logout (optional - client deletes token).

    Server-side: Add token to blacklist (if using token revocation).
    Client-side: Delete token from SecureStore.
    """
    # Optional: Add token to blacklist
    token = credentials.credentials
    await db.token_blacklist.insert_one({
        "token": token,
        "blacklisted_at": datetime.datetime.utcnow()
    })

    return None


# ============================================================================
# Preferences Endpoints
# ============================================================================

class PreferencesRequest(BaseModel):
    interests: List[str]
    foodPreferences: List[str]
    budget: str  # 'budget', 'moderate', 'luxury'
    travelDates: Optional[str] = None

class PreferencesResponse(BaseModel):
    interests: List[str]
    foodPreferences: List[str]
    budget: str
    travelDates: Optional[str]

@router.post("/preferences", response_model=PreferencesResponse)
async def save_preferences(
    request: PreferencesRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Save user preferences for trip personalization.

    Requirements:
    - JWT authentication
    - Upsert preferences (update if exists, insert if new)

    Returns:
    - Saved preferences
    """
    user_id = get_user_id_from_token(credentials.credentials)

    await db.preferences.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "interests": request.interests,
            "food_preferences": request.foodPreferences,
            "budget": request.budget,
            "travel_dates": request.travelDates,
            "updated_at": datetime.datetime.utcnow()
        }},
        upsert=True
    )

    return PreferencesResponse(**request.dict())


@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get user preferences.

    Returns:
    - Saved preferences or null if none exist
    """
    user_id = get_user_id_from_token(credentials.credentials)

    prefs = await db.preferences.find_one({"user_id": user_id})
    if not prefs:
        return None

    return PreferencesResponse(
        interests=prefs.get("interests", []),
        foodPreferences=prefs.get("food_preferences", []),
        budget=prefs.get("budget", "moderate"),
        travelDates=prefs.get("travel_dates")
    )


# ============================================================================
# City Recommendation Endpoints
# ============================================================================

class CityRecommendation(BaseModel):
    id: str
    name: str
    country: str
    reasoning: str
    imageUrl: Optional[str] = None

@router.get("/cities/recommendations", response_model=List[CityRecommendation])
async def get_city_recommendations(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get top 3 city recommendations based on user preferences.

    Requirements:
    - JWT authentication
    - User must have saved preferences
    - Call existing City Selection Agent

    Returns:
    - Top 3 cities with reasoning
    """
    user_id = get_user_id_from_token(credentials.credentials)

    # Get user preferences
    prefs = await db.preferences.find_one({"user_id": user_id})
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please set your preferences first"
        )

    # Call City Selection Agent (existing logic)
    from timbuktoo.agents.city_selection import CitySelectionAgent
    agent = CitySelectionAgent()
    cities = await agent.select_cities(
        interests=prefs["interests"],
        food_preferences=prefs.get("food_preferences", []),
        budget=prefs.get("budget", "moderate")
    )

    # Return top 3
    return [
        CityRecommendation(
            id=city["city_id"],
            name=city["name"],
            country=city["country"],
            reasoning=city["reasoning"],
            imageUrl=city.get("image_url")
        )
        for city in cities[:3]
    ]


# ============================================================================
# Itinerary Endpoints
# ============================================================================

class ItineraryRequest(BaseModel):
    cityId: str

class Activity(BaseModel):
    time: str
    name: str
    description: str
    address: str

class Meal(BaseModel):
    type: str  # breakfast, lunch, dinner
    name: str
    cuisine: str
    price: str

class DayPlan(BaseModel):
    day: int
    activities: List[Activity]
    meals: List[Meal]
    weather: str

class ItineraryResponse(BaseModel):
    itineraryId: str
    itinerary: List[DayPlan]

@router.post("/itinerary/generate", response_model=ItineraryResponse)
async def generate_itinerary(
    request: ItineraryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Generate full itinerary for selected city.

    Requirements:
    - JWT authentication
    - Call existing multi-agent workflow
    - Store itinerary for feedback

    Returns:
    - Itinerary ID
    - Day-by-day itinerary (meals, activities, weather)

    NOTE: This endpoint may take 30-60 seconds (mobile shows loading screen).
    """
    user_id = get_user_id_from_token(credentials.credentials)

    # Get user preferences
    prefs = await db.preferences.find_one({"user_id": user_id})
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please set your preferences first"
        )

    # Call multi-agent workflow (existing logic)
    from timbuktoo.workflows.orchestrator import TripOrchestrator
    orchestrator = TripOrchestrator()

    result = await orchestrator.generate_trip(
        user_id=user_id,
        city_id=request.cityId,
        preferences=prefs
    )

    # Store itinerary
    itinerary_id = str(uuid.uuid4())
    await db.itineraries.insert_one({
        "itinerary_id": itinerary_id,
        "user_id": user_id,
        "city_id": request.cityId,
        "itinerary": result["itinerary"],
        "created_at": datetime.datetime.utcnow(),
        "platform": "mobile"
    })

    # Format response
    itinerary = [
        DayPlan(
            day=day["day"],
            activities=[Activity(**act) for act in day["activities"]],
            meals=[Meal(**meal) for meal in day["meals"]],
            weather=day["weather"]
        )
        for day in result["itinerary"]
    ]

    return ItineraryResponse(itineraryId=itinerary_id, itinerary=itinerary)


# ============================================================================
# Feedback Endpoints
# ============================================================================

class FeedbackRequest(BaseModel):
    itineraryId: str
    rating: Optional[str] = None  # 'helpful', 'not-helpful'
    reportType: Optional[str] = None  # 'inaccurate', 'inappropriate', 'missing', 'other'
    comments: Optional[str] = None

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    request: FeedbackRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Submit feedback or report issue on itinerary.

    CRITICAL: Required for App Store approval (AI content moderation).

    Requirements:
    - JWT authentication
    - At least one of: rating, reportType
    - Store for compliance and product improvement

    Returns:
    - Success confirmation
    """
    user_id = get_user_id_from_token(credentials.credentials)

    await db.feedback.insert_one({
        "feedback_id": str(uuid.uuid4()),
        "user_id": user_id,
        "itinerary_id": request.itineraryId,
        "rating": request.rating,
        "report_type": request.reportType,
        "comments": request.comments,
        "created_at": datetime.datetime.utcnow(),
        "platform": "mobile",
        "reviewed": False
    })

    # If report type is "inappropriate", flag for immediate review
    if request.reportType in ["inaccurate", "inappropriate"]:
        await send_alert_to_compliance_team(request.itineraryId, request.reportType)

    return {"message": "Feedback submitted successfully"}


# ============================================================================
# User Management Endpoints
# ============================================================================

@router.delete("/user/account", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Delete user account and all data (GDPR/CCPA compliance).

    CRITICAL: Required for App Store approval (data deletion).

    Requirements:
    - JWT authentication
    - Delete user, preferences, itineraries, feedback
    - 30-day deletion SLA

    Returns:
    - Success confirmation (204 No Content)
    """
    user_id = get_user_id_from_token(credentials.credentials)

    # Delete user data
    await db.users.delete_one({"user_id": user_id})
    await db.preferences.delete_many({"user_id": user_id})
    await db.itineraries.delete_many({"user_id": user_id})
    await db.feedback.delete_many({"user_id": user_id})

    # Log deletion request (for compliance audit trail)
    await db.deletion_requests.insert_one({
        "user_id": user_id,
        "requested_at": datetime.datetime.utcnow(),
        "platform": "mobile",
        "status": "completed"
    })

    return None


# ============================================================================
# Helper Functions
# ============================================================================

def get_user_id_from_token(token: str) -> str:
    """
    Extract user_id from JWT token.

    Raises:
    - HTTPException if token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def send_alert_to_compliance_team(itinerary_id: str, report_type: str):
    """
    Send alert to compliance team for flagged content.

    Integration:
    - Slack #compliance-alerts channel
    - Email to compliance@timbuktoo.ai
    - Create Jira ticket (if high-severity)
    """
    # Slack alert
    await slack_client.post_message(
        channel="#compliance-alerts",
        text=f"🚨 Mobile user reported {report_type} content in itinerary {itinerary_id}"
    )

    # Email alert (async)
    # Jira ticket (if inappropriate content)


# ============================================================================
# Health Check
# ============================================================================

@router.get("/health")
async def health_check():
    """
    Health check endpoint for mobile app.

    Returns:
    - API status
    - Version
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "platform": "mobile"
    }
```

**Deployment Notes**:

1. **Environment Variables**:
   ```bash
   JWT_SECRET=<generate-secure-secret>
   DATABASE_URL=postgresql://...
   SLACK_WEBHOOK_URL=https://hooks.slack.com/...
   ```

2. **Database Indexes** (for performance):
   ```sql
   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_preferences_user_id ON preferences(user_id);
   CREATE INDEX idx_itineraries_user_id ON itineraries(user_id);
   CREATE INDEX idx_feedback_itinerary_id ON feedback(itinerary_id);
   ```

3. **Rate Limiting** (Cloudflare or Nginx):
   ```
   /auth/signup: 3 requests / hour / IP
   /auth/login: 10 requests / hour / IP
   /itinerary/generate: 5 requests / hour / user
   ```

4. **Monitoring**:
   - Alert if `/itinerary/generate` takes > 90 seconds
   - Alert if feedback with `reportType=inappropriate` is submitted
   - Track JWT token expiration errors

---

**API Documentation**: Generate OpenAPI/Swagger docs via FastAPI's built-in `/docs` endpoint.

**Security**: All endpoints use HTTPS (TLS 1.2+), JWT authentication, rate limiting, and input validation.
