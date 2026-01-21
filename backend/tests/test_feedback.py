"""
Tests for feedback submission endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestFeedbackSubmission:
    """Test suite for feedback submission functionality"""

    def test_submit_feedback_without_auth(self):
        """Should return 401 when not authenticated"""
        response = client.post(
            "/feedback",
            json={
                "itinerary_id": "00000000-0000-0000-0000-000000000000",
                "feedback_type": "inaccurate",
                "comments": "Test feedback"
            }
        )
        assert response.status_code == 401

    @pytest.mark.slow
    def test_submit_feedback_success(self, user_with_preferences):
        """Should successfully submit feedback"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary first
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Amsterdam",
                "country": "Netherlands",
                "trip_length_days": 3
            }
        )
        itinerary_id = create_response.json()["id"]

        # Submit feedback
        response = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "inaccurate",
                "comments": "Restaurant doesn't exist anymore"
            }
        )
        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert "itinerary_id" in data
        assert "feedback_type" in data
        assert "comments" in data
        assert "status" in data
        assert "created_at" in data

        assert data["itinerary_id"] == itinerary_id
        assert data["feedback_type"] == "inaccurate"
        assert data["comments"] == "Restaurant doesn't exist anymore"
        assert data["status"] == "pending"

    @pytest.mark.slow
    def test_submit_feedback_without_comments(self, user_with_preferences):
        """Should successfully submit feedback without comments"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary first
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Prague",
                "country": "Czech Republic",
                "trip_length_days": 2
            }
        )
        itinerary_id = create_response.json()["id"]

        # Submit feedback without comments
        response = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "inappropriate"
            }
        )
        assert response.status_code == 201
        data = response.json()

        assert data["feedback_type"] == "inappropriate"
        assert data["comments"] is None

    def test_submit_feedback_missing_itinerary_id(self, create_user):
        """Should return 422 when itinerary_id is missing"""
        user_data = create_user()
        response = client.post(
            "/feedback",
            headers={"Authorization": f"Bearer {user_data['token']}"},
            json={
                "feedback_type": "inaccurate",
                "comments": "Test"
            }
        )
        assert response.status_code == 422

    def test_submit_feedback_missing_feedback_type(self, create_user):
        """Should return 422 when feedback_type is missing"""
        user_data = create_user()
        response = client.post(
            "/feedback",
            headers={"Authorization": f"Bearer {user_data['token']}"},
            json={
                "itinerary_id": "00000000-0000-0000-0000-000000000000",
                "comments": "Test"
            }
        )
        assert response.status_code == 422

    def test_submit_feedback_invalid_type(self, create_user):
        """Should return 422 for invalid feedback type"""
        user_data = create_user()
        response = client.post(
            "/feedback",
            headers={"Authorization": f"Bearer {user_data['token']}"},
            json={
                "itinerary_id": "00000000-0000-0000-0000-000000000000",
                "feedback_type": "invalid_type",
                "comments": "Test"
            }
        )
        assert response.status_code == 422

    @pytest.mark.slow
    def test_submit_feedback_all_types(self, user_with_preferences):
        """Should accept all valid feedback types"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary first
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Vienna",
                "country": "Austria",
                "trip_length_days": 3
            }
        )
        itinerary_id = create_response.json()["id"]

        valid_types = ["inaccurate", "inappropriate", "missing_information", "other"]

        for feedback_type in valid_types:
            response = client.post(
                "/feedback",
                headers=headers,
                json={
                    "itinerary_id": itinerary_id,
                    "feedback_type": feedback_type,
                    "comments": f"Testing {feedback_type} feedback"
                }
            )
            assert response.status_code == 201
            assert response.json()["feedback_type"] == feedback_type

    @pytest.mark.slow
    def test_submit_feedback_long_comments(self, user_with_preferences):
        """Should accept long comments"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary first
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Budapest",
                "country": "Hungary",
                "trip_length_days": 3
            }
        )
        itinerary_id = create_response.json()["id"]

        # Submit feedback with long comment (500 chars)
        long_comment = "A" * 500
        response = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "other",
                "comments": long_comment
            }
        )
        assert response.status_code == 201
        assert response.json()["comments"] == long_comment

    @pytest.mark.slow
    def test_submit_multiple_feedback_same_itinerary(self, user_with_preferences):
        """Should allow multiple feedback submissions for same itinerary"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary first
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Copenhagen",
                "country": "Denmark",
                "trip_length_days": 2
            }
        )
        itinerary_id = create_response.json()["id"]

        # Submit first feedback
        response1 = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "inaccurate",
                "comments": "First issue"
            }
        )
        assert response1.status_code == 201

        # Submit second feedback for same itinerary
        response2 = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "missing_information",
                "comments": "Second issue"
            }
        )
        assert response2.status_code == 201

        # Should be different feedback IDs
        assert response1.json()["id"] != response2.json()["id"]

    def test_submit_feedback_with_invalid_token(self):
        """Should return 401 with invalid token"""
        response = client.post(
            "/feedback",
            headers={"Authorization": "Bearer invalid_token_123"},
            json={
                "itinerary_id": "00000000-0000-0000-0000-000000000000",
                "feedback_type": "inaccurate"
            }
        )
        assert response.status_code == 401

    @pytest.mark.slow
    def test_feedback_compliance_alert(self, user_with_preferences):
        """Should trigger compliance alert for inappropriate/inaccurate reports"""
        token = user_with_preferences['token']
        headers = {"Authorization": f"Bearer {token}"}

        # Create itinerary
        create_response = client.post(
            "/itinerary",
            headers=headers,
            json={
                "city_name": "Stockholm",
                "country": "Sweden",
                "trip_length_days": 3
            }
        )
        itinerary_id = create_response.json()["id"]

        # Submit inappropriate feedback (should trigger alert in logs)
        response = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "inappropriate",
                "comments": "Contains offensive content"
            }
        )
        assert response.status_code == 201

        # Submit inaccurate feedback (should trigger alert in logs)
        response = client.post(
            "/feedback",
            headers=headers,
            json={
                "itinerary_id": itinerary_id,
                "feedback_type": "inaccurate",
                "comments": "Factually incorrect information"
            }
        )
        assert response.status_code == 201

        # Note: Actual compliance alert verification would require
        # checking logs or Slack webhook calls (in production)
