"""
Tests for preferences endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def create_user():
    """Fixture to create a test user and return token"""
    import random
    response = client.post(
        "/auth/signup",
        json={
            "email": f"testuser{random.randint(1000, 99999)}@example.com",
            "password": "TestPassword123",
            "ai_disclosure_accepted": True,
            "data_use_accepted": True,
        },
    )
    return response.json()["access_token"]


class TestPreferences:
    """Test preferences endpoints"""

    def test_save_preferences_success(self, create_user):
        """Test successful preferences save"""
        token = create_user

        response = client.post(
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

        assert response.status_code == 200
        data = response.json()
        assert len(data["interests"]) == 2
        assert data["budget_level"] == "mid-range"
        assert data["trip_length_days"] == 5

    def test_save_preferences_without_auth(self):
        """Test saving preferences without authentication"""
        response = client.post(
            "/preferences",
            json={
                "interests": ["Culture & Museums"],
                "budget_level": "mid-range",
                "pace": "moderate",
                "trip_length_days": 3,
            },
        )

        assert response.status_code == 401

    def test_save_preferences_invalid_trip_length(self, create_user):
        """Test saving preferences with invalid trip length"""
        token = create_user

        response = client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "interests": ["Culture & Museums"],
                "budget_level": "mid-range",
                "pace": "moderate",
                "trip_length_days": 50,  # Too long
            },
        )

        assert response.status_code == 422

    def test_save_preferences_invalid_budget(self, create_user):
        """Test saving preferences with invalid budget level"""
        token = create_user

        response = client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "interests": ["Culture & Museums"],
                "budget_level": "invalid",
                "pace": "moderate",
                "trip_length_days": 5,
            },
        )

        assert response.status_code == 422

    def test_get_preferences_success(self, create_user):
        """Test retrieving saved preferences"""
        token = create_user

        # Save preferences first
        client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "interests": ["Nature & Outdoors"],
                "food_preferences": ["Vegan"],
                "budget_level": "luxury",
                "pace": "relaxed",
                "trip_length_days": 7,
            },
        )

        # Get preferences
        response = client.get(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["budget_level"] == "luxury"
        assert data["trip_length_days"] == 7

    def test_get_preferences_not_found(self, create_user):
        """Test getting preferences when none exist"""
        token = create_user

        response = client.get(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404

    def test_update_preferences(self, create_user):
        """Test updating existing preferences"""
        token = create_user

        # Save initial preferences
        client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "interests": ["Culture & Museums"],
                "budget_level": "budget",
                "pace": "moderate",
                "trip_length_days": 3,
            },
        )

        # Update preferences
        response = client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "interests": ["Culture & Museums", "Shopping"],
                "budget_level": "mid-range",  # Changed
                "pace": "packed",  # Changed
                "trip_length_days": 5,  # Changed
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["interests"]) == 2
        assert data["budget_level"] == "mid-range"
        assert data["trip_length_days"] == 5
