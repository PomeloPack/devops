import pytest
from backend.weather_app import app as flask_app, db

@pytest.fixture
def app():
    """Return the Flask app for testing."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()