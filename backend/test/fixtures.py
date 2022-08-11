from app import create_app

import pytest
from pytest_mock import mocker

from test.mock.mock_mail import mailbox

@pytest.fixture()
def app(mocker):
    # Mock only where the data is being used
    mocker.patch("app.mail", mailbox)
    mocker.patch("common.plugins.mail", mailbox)
    mocker.patch("routes.auth.mail", mailbox)

    app = create_app({"TESTING": True})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
