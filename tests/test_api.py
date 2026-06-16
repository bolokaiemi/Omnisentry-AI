
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


def test_admin_verify_success():
    response = client.post(
        "/api/admin/verify",
        json={"password": "admin123"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_admin_verify_incorrect():
    response = client.post(
        "/api/admin/verify",
        json={"password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect admin password" in response.json()["detail"]


def test_about_page():
    response = client.get("/about")
    assert response.status_code == 200


def test_contact_page():
    response = client.get("/contact")
    assert response.status_code == 200


def test_services_page():
    response = client.get("/services")
    assert response.status_code == 200


def test_admin_login_page():
    response = client.get("/admin/login")
    assert response.status_code == 200




