"""
Tests for authentication endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestSignup:
    """Test user signup endpoint"""

    def test_signup_success(self):
        """Test successful user signup"""
        response = client.post(
            "/auth/signup",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"

    def test_signup_missing_email(self):
        """Test signup with missing email"""
        response = client.post(
            "/auth/signup",
            json={
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        assert response.status_code == 422  # Validation error

    def test_signup_invalid_email(self):
        """Test signup with invalid email format"""
        response = client.post(
            "/auth/signup",
            json={
                "email": "invalid-email",
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        assert response.status_code == 422

    def test_signup_weak_password(self):
        """Test signup with weak password"""
        response = client.post(
            "/auth/signup",
            json={
                "email": "test2@example.com",
                "password": "weak",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        assert response.status_code == 400
        assert "password" in response.json()["detail"].lower()

    def test_signup_duplicate_email(self):
        """Test signup with already registered email"""
        # First signup
        client.post(
            "/auth/signup",
            json={
                "email": "duplicate@example.com",
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        # Second signup with same email
        response = client.post(
            "/auth/signup",
            json={
                "email": "duplicate@example.com",
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        assert response.status_code == 409  # Conflict
        assert "exists" in response.json()["detail"].lower()

    def test_signup_ai_disclosure_not_accepted(self):
        """Test signup without accepting AI disclosure"""
        response = client.post(
            "/auth/signup",
            json={
                "email": "test3@example.com",
                "password": "TestPassword123",
                "ai_disclosure_accepted": False,
                "data_use_accepted": True,
            },
        )

        assert response.status_code == 400
        assert "ai disclosure" in response.json()["detail"].lower()


class TestLogin:
    """Test user login endpoint"""

    def test_login_success(self):
        """Test successful login"""
        # Create user first
        client.post(
            "/auth/signup",
            json={
                "email": "login@example.com",
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        # Login
        response = client.post(
            "/auth/login",
            json={
                "email": "login@example.com",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        # Create user first
        client.post(
            "/auth/signup",
            json={
                "email": "wrongpass@example.com",
                "password": "TestPassword123",
                "ai_disclosure_accepted": True,
                "data_use_accepted": True,
            },
        )

        # Login with wrong password
        response = client.post(
            "/auth/login",
            json={
                "email": "wrongpass@example.com",
                "password": "WrongPassword123",
            },
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 401


@pytest.fixture
def auth_token():
    """Fixture to create a user and return auth token"""
    response = client.post(
        "/auth/signup",
        json={
            "email": f"fixture{pytest.gen.randint(1000, 9999)}@example.com",
            "password": "TestPassword123",
            "ai_disclosure_accepted": True,
            "data_use_accepted": True,
        },
    )
    return response.json()["access_token"]


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    response = client.get("/user/me")
    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token():
    """Test accessing protected endpoint with invalid token"""
    response = client.get(
        "/user/me",
        headers={"Authorization": "Bearer invalid_token_123"},
    )
    assert response.status_code == 401
