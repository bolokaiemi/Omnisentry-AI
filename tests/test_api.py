
# ==========================================
# TEST API
# ==========================================

from fastapi.testclient import TestClient

from app import app


client = TestClient(
    app
)


def test_home():

    response = client.get(
        "/"
    )

    assert response.status_code == 200


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "online"


def test_info():

    response = client.get(
        "/info"
    )

    assert response.status_code == 200


def test_check_domain():

    response = client.get(
        "/check/google.com"
    )

    assert response.status_code == 200

    data = response.json()

    assert "success" in data


def test_score():

    response = client.get(
        "/score/google.com"
    )

    assert response.status_code == 200

