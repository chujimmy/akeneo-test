import pytest

from secret_santa_api import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///secret_santa_test.db",
        }
    )

    with app.test_client() as client:
        yield client
