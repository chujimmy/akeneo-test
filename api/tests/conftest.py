import pytest

from secret_santa_api import create_app


@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///secret_santa_test.db",
        }
    )

    return app


@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client
