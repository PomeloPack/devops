import pytest

@pytest.mark.parametrize("endpoint,expected_status", [
    ("/health", 200),
    ("/cities", 200)
])
def test_endpoints(client, endpoint, expected_status):
    response = client.get(endpoint)
    assert response.status_code == expected_status

def test_cities_content(client):
    response = client.get("/cities")
    data = response.get_json()
    assert isinstance(data, list)
    assert "New York" in data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"