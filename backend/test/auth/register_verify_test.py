import email
import os
import poplib
import re
from datetime import datetime, timedelta

import fakeredis
import pytest
from freezegun import freeze_time
from pytest_mock import mocker

# Imports for pytest
import common
from test.helpers import clear_all, get_most_recent_email
from test.fixtures import app, client

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
@pytest.mark.skip()
def test_token_expired(client, mocker):
    fake = fakeredis.FakeStrictRedis()
    mocker.patch.object(common.redis, "cache", return_value=fake)

    register_response = client.post("/auth/register", json={
        "email": "asdfghjkl@gmail.com",
        "username": "asdf",
        "password": "foobar"
    })

    print(fake.keys())

    assert register_response.status_code == 200

    # Check inbox
    parsed_email = get_most_recent_email()

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()

    # Extract the token from the HTML
    token = find_token(content)

    expired_time = datetime.now() + timedelta(hours=2)

    with freeze_time(expired_time):
        print(fake.keys())

        response = client.post("/auth/register/verify", json={
            "token": token
        })

        assert response.status_code == 401

@pytest.mark.email
def test_success(client):
    clear_all()

    register_response = client.post("/auth/register", json={
        "email": "asdfghjkl@gmail.com",
        "username": "asdf",
        "password": "foobar"
    })

    assert register_response.status_code == 200

    # Check inbox
    parsed_email = get_most_recent_email()

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
