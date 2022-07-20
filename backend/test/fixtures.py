<<<<<<< HEAD
import pytest

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
=======
import pytest

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
>>>>>>> ffb4c6ef4ed862c6fec20a1167c30d75808de300
