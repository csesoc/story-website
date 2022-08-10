import email
import os
import poplib
import requests

# Imports for pytest
import pytest

from test.helpers import clear_all, db_add_user
from test.fixtures import app, client


def register(json):
    response = requests.post(
        f"{os.environ['TESTING_ADDRESS']}/auth/register", json=json)
    return response


def test_invalid_email(client):
    clear_all()

    # Frontend should detect whether an email address doesn't follow a
    # specific format, so we don't have to handle those errors here
    invalid_address = "foo@guaranteed.invalid"

    response = client.post("/auth/register", json={
        "email": invalid_address,
        "username": "Test",
        "password": "foobar123"
    })

    assert response.status_code == 400


def test_duplicate_email(client):
    clear_all()

    reused_address = "asdfghjkl@gmail.com"

    # Register the user in the database directly, to avoid another email
    db_add_user(reused_address, "foo", "bar")

    response = client.post("/auth/register", json={
        "email": reused_address,
        "username": "foo",
        "password": "bar"
    })

    assert response.status_code == 400


def test_duplicate_username(client):
    clear_all()

    reused_username = "foo"

    # Register the user in the database directly
    db_add_user("asdfghjkl@gmail.com", reused_username, "bar")

    response = client.post("/auth/register", json={
        "email": "foobar@gmail.com",
        "username": reused_username,
        "password": "bar"
    })

    assert response.status_code == 400


@pytest.mark.email
def test_success(client):
    clear_all()

    # Check that we get an email sent
    mailbox = poplib.POP3("pop3.mailtrap.io", 1100)
    mailbox.user(os.environ["MAILTRAP_USERNAME"])
    mailbox.pass_(os.environ["MAILTRAP_PASSWORD"])

    (before, _) = mailbox.stat()

    # Register normally
    response = client.post("/auth/register", json={
        "email": "asdfghjkl@gmail.com",
        "username": "asdf",
        "password": "foobar123"
    })

    assert response.status_code == 200

    # Check that an email was in fact sent
    (after, _) = mailbox.stat()

    assert after == before + 1

    # Verify recipient
    raw_email = b"\n".join(mailbox.retr(1)[1])
    parsed_email = email.message_from_bytes(raw_email)

    assert parsed_email["To"] == "asdfghjkl@gmail.com"
