import pytest

from test.mock.mock_mail import mailbox
from test.mock.mock_redis import fake_redis

from app import create_app

@pytest.fixture()
def app(mocker):
    # Mock mailbox
    mocker.patch("app.mail", mailbox)
    mocker.patch("common.plugins.mail", mailbox)

    # Mock redis
    mocker.patch("common.redis.cache", fake_redis)

    app = create_app({"TESTING": True})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
