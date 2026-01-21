"""
Tests for itinerary generation and management endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestItineraryGeneration:
    """Test suite for itinerary generation"""

    def test_generate_itinerary_without_auth(self):
        """Should return 401 when not authenticated"""
        response = client.post(
            "/itinerary",
            json={
                "city_name": "Paris",
                "country": "France",
                "trip_length_days": 3
            }
        )
        assert response.status_code == 401

    def test_generate_itinerary_without_preferences(self, create_user):
        """Should return 400 when user has no preferences"""
        user_data = create_user()
        response = client.post(
            "/itinerary",
            headers={"Authorization": f"Bearer {user_data['token']}"},
            json={
                "city_name": "Paris",
                "country": "France",
                "trip_length_days": 3
            }
        )
        assert response.status_code == 400
        assert "preferences" in response.json()["detail"].lower()

    def test_generate_itinerary_invalid_trip_length(self, user_with_preferences):
        """Should return 422 for invalid trip length"""
        # Too short
        response = client.post(
            "/itinerary",
            headers={"Authorization": f"Bearer {user_with_preferences['token']}"},
            json={
                "city_name": "Paris",
                "country": "France",
                "trip_length_days": 0
            }
        )
        assert response.status_code == 422

        # Too long
        response = client.post(
            "/itinerary",
            headers={"Authorization": f"Bearer {user_with_preferences['token']}"},
            json={
                "city_name": "Paris",
                "country": "France",
                "trip_length_days": 31
            }
        )
        assert response.status_code == 422

    def test_generate_itinerary_missing_city(self, user_with_preferences):
        """Should return 422 when city information is missing"""
        response = client.post(
            "/itinerary",
            headers={"Authorization": f"Bearer {user_with_preferences['token']}"},
            json={
                "trip_length_days": 3
            }
        )
        assert response.status_code == 422

    @pytest.mark.slow
    def test_generate_itinerary_success(self, user_with_preferences):
        """Should successfully generate itinerary"""
        response = client.post(
            "/itinerary",
            headers={"Authorization": f"Bearer {user_with_preferences['token']}"},
            json={
                "city_name": "Paris",
                "country": "France",
                "trip_length_days": 3
            }
        )
        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert "city_name" in data
        assert "country" in data
        assert "itinerary_data" in data
        assert "trip_length_days" in data

        assert data["city_name"] == "Paris"
        assert data["country"] == "France"
        assert data["trip_length_days"] == 3

        # Verify itinerary_data structure
        itinerary_data = data["itinerary_data"]
        assert "daily_plans" in itinerary_data
        assert "general_tips" in itinerary_data
        assert len(itinerary_data["daily_plans"]) == 3

        # Verify daily plan structure
        for day_plan in itinerary_data["daily_plans"]:
            assert "day" in day_plan
            assert "morning" in day_plan
            assert "lunch" in day_plan
            assert "afternoon" in day_plan
            assert "dinner" in day_plan

            # Verify morning/afternoon structure
            assert "activity" in day_plan["morning"]
            assert "location" in day_plan["morning"]
            assert "duration" in day_plan["morning"]
            assert "tips" in day_plan["morning"]

            # Verify lunch/dinner structure
            assert "restaurant" in day_plan["lunch"]
            assert "cuisine" in day_plan["lunch"]
            assert "price_range" in day_plan["lunch"]

    def test_generate_itinerary_free_tier_limit(self, user_with_preferences):
        """Should enforce free tier limit (3 itineraries)"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Generate 3 itineraries (free tier limit)
        for i in range(3):
            response = client.post(
                "/itinerary",
                headers=headers,
                json={
                    "city_name": f"City{i}",
                    "country": "Country",
                    "trip_length_days": 2
                }
            )
            assert response.status_code == 201

        # 4th itinerary should be blocked
        response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "City4",
                "country": "Country",
                "trip_length_days": 2
            }
        )
        assert response.status_code == 403
        assert "limit" in response.json()["detail"].lower()


class TestItineraryRetrieval:
    """Test suite for itinerary retrieval endpoints"""

    def test_get_user_itineraries_without_auth(self):
        """Should return 401 when not authenticated"""
        response = client.get("/itineraries")
        assert response.status_code == 401

    def test_get_user_itineraries_empty(self, create_user):
        """Should return empty list when user has no itineraries"""
        user_data = create_user()
        response = client.get(
            "/itineraries",
            headers={"Authorization": f"Bearer {user_data['token']}"}
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.slow
    def test_get_user_itineraries_success(self, user_with_preferences):
        """Should return user's itineraries"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Tokyo",
                "country": "Japan",
                "trip_length_days": 5
            }
        )
        assert create_response.status_code == 201

        # Get all itineraries
        response = client.get("/itineraries", headers=headers)
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) >= 1

        # Verify itinerary structure
        itinerary = data[0]
        assert "id" in itinerary
        assert "city_name" in itinerary
        assert "created_at" in itinerary

    @pytest.mark.slow
    def test_get_itinerary_by_id_success(self, user_with_preferences):
        """Should return specific itinerary by ID"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "London",
                "country": "UK",
                "trip_length_days": 4
            }
        )
        itinerary_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/itinerary/{itinerary_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()

        assert data["id"] == itinerary_id
        assert data["city_name"] == "London"
        assert data["country"] == "UK"

    def test_get_itinerary_by_id_not_found(self, create_user):
        """Should return 404 for non-existent itinerary"""
        user_data = create_user()
        response = client.get(
            "/itinerary/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": f"Bearer {user_data['token']}"}
        )
        assert response.status_code == 404

    @pytest.mark.slow
    def test_get_itinerary_by_id_unauthorized(self, user_with_preferences, create_user):
        """Should return 404 when accessing another user's itinerary"""
        # User 1 creates itinerary
        user1_token = user_with_preferences['token']
        create_response = client.post(
            "/itinerary",
            headers={"Authorization": f"Bearer {user1_token}"},
            json={
                "city_name": "Rome",
                "country": "Italy",
                "trip_length_days": 3
            }
        )
        itinerary_id = create_response.json()["id"]

        # User 2 tries to access it
        user2 = create_user(email="user2@test.com")
        response = client.get(
            f"/itinerary/{itinerary_id}",
            headers={"Authorization": f"Bearer {user2['token']}"}
        )
        assert response.status_code == 404  # Not found (security best practice)


class TestItineraryRating:
    """Test suite for itinerary rating functionality"""

    @pytest.mark.slow
    def test_rate_itinerary_helpful(self, user_with_preferences):
        """Should successfully rate itinerary as helpful"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Barcelona",
                "country": "Spain",
                "trip_length_days": 3
            }
        )
        itinerary_id = create_response.json()["id"]

        # Rate as helpful
        response = client.patch(
            f"/itinerary/{itinerary_id}/rating",
            headers=headers,
            json={"helpful": True}
        )
        assert response.status_code == 200
        assert response.json()["helpful_rating"] == "helpful"

    @pytest.mark.slow
    def test_rate_itinerary_not_helpful(self, user_with_preferences):
        """Should successfully rate itinerary as not helpful"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Berlin",
                "country": "Germany",
                "trip_length_days": 4
            }
        )
        itinerary_id = create_response.json()["id"]

        # Rate as not helpful
        response = client.patch(
            f"/itinerary/{itinerary_id}/rating",
            headers=headers,
            json={"helpful": False}
        )
        assert response.status_code == 200
        assert response.json()["helpful_rating"] == "not_helpful"

    def test_rate_itinerary_not_found(self, create_user):
        """Should return 404 for non-existent itinerary"""
        user_data = create_user()
        response = client.patch(
            "/itinerary/00000000-0000-0000-0000-000000000000/rating",
            headers={"Authorization": f"Bearer {user_data['token']}"},
            json={"helpful": True}
        )
        assert response.status_code == 404
