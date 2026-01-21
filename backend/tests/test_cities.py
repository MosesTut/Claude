"""
Tests for city recommendation endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCityRecommendations:
    """Test suite for city recommendation functionality"""

    def test_get_cities_without_auth(self):
        """Should return 401 when not authenticated"""
        response = client.get("/cities")
        assert response.status_code == 401

    def test_get_cities_without_preferences(self, create_user):
        """Should return 400 when user has no preferences"""
        user_data = create_user()
        response = client.get(
            "/cities",
            headers={"Authorization": f"Bearer {user_data['token']}"}
        )
        assert response.status_code == 400
        assert "preferences" in response.json()["detail"].lower()

    def test_get_cities_success(self, user_with_preferences):
        """Should return city recommendations when user has preferences"""
        response = client.get(
            "/cities",
            headers={"Authorization": f"Bearer {user_with_preferences['token']}"}
        )
        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "cities" in data
        assert isinstance(data["cities"], list)
        assert len(data["cities"]) == 3  # Should return 3 cities

        # Verify each city has required fields
        for city in data["cities"]:
            assert "city_name" in city
            assert "country" in city
            assert "reasoning" in city
            assert isinstance(city["city_name"], str)
            assert isinstance(city["country"], str)
            assert isinstance(city["reasoning"], str)
            assert len(city["city_name"]) > 0
            assert len(city["country"]) > 0
            assert len(city["reasoning"]) > 0

    def test_get_cities_cached(self, user_with_preferences):
        """Should return same cities on repeated requests (caching)"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # First request
        response1 = client.get("/cities", headers=headers)
        assert response1.status_code == 200
        cities1 = response1.json()["cities"]

        # Second request (should be cached)
        response2 = client.get("/cities", headers=headers)
        assert response2.status_code == 200
        cities2 = response2.json()["cities"]

        # Should return same cities
        assert cities1 == cities2

    def test_get_cities_different_preferences(self, create_user):
        """Should return different cities for different preferences"""
        # User 1 with culture preferences
        user1 = create_user(email="user1@test.com")
        client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {user1['token']}"},
            json={
                "interests": ["Culture & Museums", "History"],
                "budget_level": "mid-range",
                "pace": "relaxed",
                "trip_length_days": 5
            }
        )
        response1 = client.get(
            "/cities",
            headers={"Authorization": f"Bearer {user1['token']}"}
        )

        # User 2 with adventure preferences
        user2 = create_user(email="user2@test.com")
        client.post(
            "/preferences",
            headers={"Authorization": f"Bearer {user2['token']}"},
            json={
                "interests": ["Adventure", "Nature & Outdoors"],
                "budget_level": "budget",
                "pace": "packed",
                "trip_length_days": 3
            }
        )
        response2 = client.get(
            "/cities",
            headers={"Authorization": f"Bearer {user2['token']}"}
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        cities1 = response1.json()["cities"]
        cities2 = response2.json()["cities"]

        # Cities should be different (AI should recommend based on preferences)
        # Note: This might occasionally fail if AI happens to recommend same cities
        city_names1 = [c["city_name"] for c in cities1]
        city_names2 = [c["city_name"] for c in cities2]

        # At least one city should be different
        assert city_names1 != city_names2 or cities1[0]["reasoning"] != cities2[0]["reasoning"]

    def test_get_cities_with_invalid_token(self):
        """Should return 401 with invalid token"""
        response = client.get(
            "/cities",
            headers={"Authorization": "Bearer invalid_token_123"}
        )
        assert response.status_code == 401

    def test_get_cities_with_malformed_auth_header(self):
        """Should return 401 with malformed Authorization header"""
        response = client.get(
            "/cities",
            headers={"Authorization": "NotBearer token123"}
        )
        assert response.status_code == 401

    @pytest.mark.slow
    def test_get_cities_performance(self, user_with_preferences):
        """Should return cities within reasonable time"""
        import time

        start_time = time.time()
        response = client.get(
            "/cities",
            headers={"Authorization": f"Bearer {user_with_preferences['token']}"}
        )
        end_time = time.time()

        assert response.status_code == 200

        # Should complete within 15 seconds (AI API call)
        assert end_time - start_time < 15.0
