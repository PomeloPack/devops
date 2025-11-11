from backend.weather_app import app, db  # importuj Flask app i db

with app.app_context():
    db.drop_all()       # smaže všechny tabulky (opatrně!)
    db.create_all()     # vytvoří nové tabulky podle aktuálního modelu

print('Created a new db with actual schema model')