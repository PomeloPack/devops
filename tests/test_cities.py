from backend.weather_app import city_list, city_timezones

def test_all_cities_have_timezone():
    """Each city in city_list must have a corresponding timezone."""
    for city in city_list:
        assert city in city_timezones, f"{city} does not have an assigned timezone"

def test_timezones_are_not_empty():
    """No timezone should be empty."""
    for city, tz in city_timezones.items():
        assert tz, f"The timezone for {city} is empty"

def test_city_and_timezone_are_strings():
    """City names and timezones should be strings."""
    for city in city_list:
        assert isinstance(city, str), f"{city} is not a string"
    for tz in city_timezones.values():
        assert isinstance(tz, str), f"{tz} is not a string"