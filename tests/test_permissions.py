from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_app_permissions():
    response = client.get("/api/app/permissions")
    assert response.status_code == 200
    
    data = response.json()
    assert "permissions" in data
    assert isinstance(data["permissions"], list)
    assert len(data["permissions"]) > 0
    
    # Check for specific expected permissions
    perm_names = [p["name"] for p in data["permissions"]]
    assert "internet" in perm_names
    assert "notifications" in perm_names
    assert "browser_activity" in perm_names
    
    # Check that required properties are present
    first_perm = data["permissions"][0]
    assert "name" in first_perm
    assert "required" in first_perm
    assert "purpose" in first_perm
