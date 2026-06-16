from fastapi.testclient import TestClient
from app import app
import pytest

client = TestClient(app)

def test_get_feedback():
    response = client.get("/api/feedback")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Since we seeded 5 reviews, it should have at least 5 reviews
    assert len(data) >= 5
    for item in data:
        assert "name" in item
        assert "rating" in item
        assert "comment" in item
        assert "timestamp" in item

def test_post_feedback_success():
    payload = {
        "name": "Test User",
        "rating": 4,
        "comment": "This is a programmatic test review."
    }
    
    # Get initial count
    initial_response = client.get("/api/feedback")
    initial_count = len(initial_response.json())
    
    # Post new feedback
    response = client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "success"
    
    # Get updated count
    updated_response = client.get("/api/feedback")
    updated_data = updated_response.json()
    assert len(updated_data) == initial_count + 1
    
    # Verify the posted content
    latest = updated_data[0]  # sorted descending by timestamp
    assert latest["name"] == "Test User"
    assert latest["rating"] == 4
    assert latest["comment"] == "This is a programmatic test review."

def test_post_feedback_invalid():
    # Invalid rating
    payload_bad_rating = {
        "name": "Bad Rating User",
        "rating": 6,
        "comment": "Rating is too high"
    }
    response = client.post("/api/feedback", json=payload_bad_rating)
    assert response.status_code == 400
    
    # Empty name
    payload_bad_name = {
        "name": "   ",
        "rating": 5,
        "comment": "Missing name"
    }
    response = client.post("/api/feedback", json=payload_bad_name)
    assert response.status_code == 400

def test_get_milestone():
    response = client.get("/api/milestone")
    assert response.status_code == 200
    data = response.json()
    assert "testers_count" in data
    assert "target_milestone" in data
    assert "total_reviews" in data
    assert "average_rating" in data
    assert "scans_count" in data
    
    assert data["target_milestone"] == 5000
    assert data["testers_count"] >= 4812
