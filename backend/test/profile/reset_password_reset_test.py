import email
import os
import poplib
import re

# Imports for pytest
from test.helpers import clear_all, db_add_user, generate_csrf_header
from test.fixtures import app, client
from test.mock.mock_mail import mailbox
from pytest_mock import mocker


## HELPER FUNCTIONS

def find_token(contents):
    verify_link = "http://localhost:5001/verify/"
    results = re.findall(rf"<a href=\"{verify_link}(.*?)\">", contents)

    return results[0]

### test starts here

def test_password_reset(client, mocker):
    clear_all()
    mocker.patch("routes.user.mail", mailbox)

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })
    assert response.status_code == 200

    profile = client.get("/user/profile")
    assert profile.status_code == 200
    assert profile.json == {
        "email": "asdfghjkl@gmail.com",
        "username": "asdf"
    }

    before = len(mailbox.messages)
    reset = client.post("/user/reset_password/request", json={
        "email": "asdfghjkl@gmail.com"
    },headers=generate_csrf_header(response))

    assert reset.status_code == 200
    after = len(mailbox.messages)
    assert after == before + 1

    # Check inbox
    parsed_email = mailbox.get_message(-1)
    assert parsed_email["To"] == "asdfghjkl@gmail.com"

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()
    # Extract the token from the HTML
    token = find_token(content)

    response2 = client.post("/user/reset_password/reset", json={
        "reset_code": token,
        "password": "ghjkl"
    }, headers=generate_csrf_header(response))

    assert response2.status_code == 200

    response = client.post("/auth/logout")

    assert response.status_code == 200

    # Check there's no more cookies
    assert len(client.cookie_jar) == 0

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "ghjkl"
    })
    
    assert response.status_code == 200

def test_password_reset_invalid_token(client, mocker):
    clear_all()
    mocker.patch("routes.user.mail", mailbox)

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })
    assert response.status_code == 200

    profile = client.get("/user/profile")
    assert profile.status_code == 200
    assert profile.json == {
        "email": "asdfghjkl@gmail.com",
        "username": "asdf"
    }

    before = len(mailbox.messages)
    reset = client.post("/user/reset_password/request", json={
        "email": "asdfghjkl@gmail.com"
    },headers=generate_csrf_header(response))

    assert reset.status_code == 200
    after = len(mailbox.messages)
    assert after == before + 1

    # Check inbox
    parsed_email = mailbox.get_message(-1)
    assert parsed_email["To"] == "asdfghjkl@gmail.com"

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()
    # Extract the token from the HTML
    token = find_token(content)

    response2 = client.post("/user/reset_password/reset", json={
        "reset_code": token,
        "password": "ghjkl"
    })

    response2.status_code == 401

def test_password_reset_wrong_code(client, mocker):
    clear_all()
    mocker.patch("routes.user.mail", mailbox)

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })
    assert response.status_code == 200

    profile = client.get("/user/profile")
    assert profile.status_code == 200
    assert profile.json == {
        "email": "asdfghjkl@gmail.com",
        "username": "asdf"
    }

    before = len(mailbox.messages)
    reset = client.post("/user/reset_password/request", json={
        "email": "asdfghjkl@gmail.com"
    },headers=generate_csrf_header(response))

    assert reset.status_code == 200
    after = len(mailbox.messages)
    assert after == before + 1

    # Check inbox
    parsed_email = mailbox.get_message(-1)
    assert parsed_email["To"] == "asdfghjkl@gmail.com"

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()
    # Extract the token from the HTML
    token = find_token(content)

    response2 = client.post("/user/reset_password/reset", json={
        "reset_code": "wrong code wrong code wrong code",
        "password": "ghjkl"
    },headers=generate_csrf_header(response))

    response2.status_code == 401