"""
Pytest configuration and shared fixtures
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import random


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up test database before all tests"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Get test client"""
    return TestClient(app)


@pytest.fixture
def create_user(client):
    """Fixture to create a test user and return token"""
    def _create_user(email=None):
        if not email:
            email = f"testuser{random.randint(10000, 99999)}@example.com"

        response = client.post(
            "/auth/signup",
            json={
                "email": email,
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        return {
            "token": response.json()["access_token"],
            "user": response.json()["user"],
        }

    return _create_user


@pytest.fixture
def auth_headers(create_user):
    """Fixture to get authorization headers"""
    user_data = create_user()
    return {"Authorization": f"Bearer {user_data['token']}"}


@pytest.fixture
def user_with_preferences(client, create_user):
    """Fixture to create user with saved preferences"""
    user_data = create_user()
    token = user_data["token"]

    # Save preferences
    client.post(
        "/preferences",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "interests": ["Culture & Museums", "Food & Dining"],
            "food_preferences": ["Vegetarian"],
            "budget_level": "mid-range",
            "pace": "moderate",
            "trip_length_days": 5,
        },
    )

    return user_data
