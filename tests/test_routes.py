def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"WeatherApp" in response.data

def test_cities_endpoint(client):
    response = client.get("/cities")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert "New York" in data