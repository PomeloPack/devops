from weather_app_with_flask import app, db, WeatherLog
import datetime as dt

with app.app_context():
    db.drop_all()   # smaže všechny tabulky podle modelů
    db.create_all() # vytvoří tabulky podle aktuálních modelů

    # vloží testovací řádek
    log = WeatherLog(
        city='TestCity',
        temp_c=20.5,
        temp_f=68.9,
        description='sunny',
        wind_speed=5.0,
        humidity=50,
        timestamp=dt.datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()

    print("Tabulka weather_log byla vytvořena a vložen testovací řádek.")