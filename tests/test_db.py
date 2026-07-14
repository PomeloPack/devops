from backend.weather_app import WeatherAppDb, db

def test_database_insert(client, app):
    # 1. ARRANGE (Příprava)
    # Vytvoříme si falešná data o počasí přesně ve formátu, jaký aplikace čeká
    test_data = {
        "city": "Testov",
        "temp_c": 25.5,
        "temp_f": 77.9,
        "description": "Sunny with occasional tests"
    }

    # 2. ACT (Akce)
    # Nasimulujeme, že aplikace posílá tato data k uložení přes POST požadavek
    response = client.post("/data", json=test_data)
    
    # Ověříme, že server odpověděl kódem 201 (Created)
    assert response.status_code == 201

    # 3. ASSERT (Ověření v databázi)
    # Musíme použít app_context, protože saháme na databázi mimo běžící požadavek
    with app.app_context():
        # Zkusíme v databázi najít město "Testov"
        saved_log = WeatherAppDb.query.filter_by(city="Testov").first()
        
        # Tvrdíme, že záznam musí existovat (nesmí být None)
        assert saved_log is not None
        
        # Tvrdíme, že teplota v databázi se přesně shoduje s tím, co jsme poslali
        assert saved_log.temp_c == 25.5
        assert saved_log.description == "Sunny with occasional tests"