import re
from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from pytest_mock import mocker

# Imports for pytest
from test.helpers import clear_all
from test.fixtures import app, client
from test.mock.mock_mail import mailbox

## HELPER FUNCTIONS

def find_token(contents):
    verify_link = "http://localhost:5001/verify/"
    results = re.findall(rf"<a href=\"{verify_link}(.*?)\">", contents)

    return results[0]

## TESTS

def test_invalid_token(client):
    clear_all()

    invalid_token = "invalid"

    response = client.post("/auth/register/verify", json={
        "token": invalid_token
    })

    assert response.status_code == 401

# TODO: try working on this, if not feasible delete this test and test manually
def test_token_expired(client, mocker):
    clear_all()

    mocker.patch("routes.auth.mail", mailbox)

    register_response = client.post("/auth/register", json={
        "email": "asdfghjkl@gmail.com",
        "username": "asdf",
        "password": "foobar"
    })

    assert register_response.status_code == 200

    # Check inbox
    parsed_email = mailbox.get_message(-1)

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()

    # Extract the token from the HTML
    token = find_token(content)

    expired_time = datetime.now() + timedelta(hours=2)

    with freeze_time(expired_time):
        response = client.post("/auth/register/verify", json={
            "token": token
        })

        assert response.status_code == 401

def test_verify_success(client, mocker):
    mocker.patch("routes.auth.mail", mailbox)

    clear_all()

    register_response = client.post("/auth/register", json={
        "email": "asdfghjkl@gmail.com",
        "username": "asdf",
        "password": "foobar"
    })

    assert register_response.status_code == 200

    # Check inbox
    parsed_email = mailbox.get_message(-1)

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()

    # Extract the token from the HTML
    token = find_token(content)

    response = client.post("/auth/register/verify", json={
        "token": token
    })

    assert response.status_code == 200
