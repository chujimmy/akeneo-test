import pytest
from dotenv import load_dotenv

from secret_santa_api import create_app


@pytest.fixture(scope="function")
def app():
    app = create_app(True)

    return app


@pytest.fixture(scope="function")
def app_context(app):
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path="./tests/.env.test")
