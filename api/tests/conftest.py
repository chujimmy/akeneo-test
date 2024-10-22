import pytest

from secret_santa_api.db import db
from secret_santa_api import create_app


@pytest.fixture(scope="function")
def app():
    app = create_app("./tests/.env.test")

    return app



@pytest.fixture(scope="function")
def app_context(app):
    with app.app_context():
        yield app

        db.session.remove()  # Remove any sessions
        db.drop_all()  # Drop all tables

@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client
