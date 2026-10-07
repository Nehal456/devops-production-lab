from app import app

def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_version_endpoint():
    client = app.test_client()

    response = client.get("/api/version")

    assert response.status_code == 200
    assert response.json["version"] == "1.0.0"