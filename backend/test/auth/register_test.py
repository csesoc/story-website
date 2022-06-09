import email
import os
import poplib
import requests

from auth.user import User
from common.database import get_connection, clear_database

def add_user(email, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    User._add_user(conn, cursor, email, username, password)

    cursor.close()
    conn.close()

def register(json):
    response = requests.post(f"{os.environ['TESTING_ADDRESS']}/auth/register", json=json)
    return response

def test_invalid_email():
    clear_database()

    # Frontend should detect whether an email address doesn't follow a
    # specific format, so we don't have to handle those errors here
    invalid_address = "foo@guaranteed.invalid"

    response = register({
        "email": invalid_address,
        "username": "Test",
        "password": "foobar123"
    })

    assert response.status_code == 400

def test_duplicate_email():
    clear_database()

    reused_address = "asdfghjkl@gmail.com"

    # Register the user in the database directly, to avoid another email
    add_user(reused_address, "foo", "bar")

    response = register({
        "email": reused_address,
        "username": "foo",
        "password": "bar"
    })

    assert response.status_code == 400

def test_duplicate_username():
    clear_database()

    reused_username = "foo"

    # Register the user in the database directly
    add_user("asdfghjkl@gmail.com", reused_username, "bar")

    response = register({
        "email": "foobar@gmail.com",
        "username": reused_username,
        "password": "bar"
    })

    assert response.status_code == 400

def test_success():
    clear_database()

    # Check that we get an email sent
    mailbox = poplib.POP3("pop3.mailtrap.io", 1100)
    mailbox.user(os.environ["MAILTRAP_USERNAME"])
    mailbox.pass_(os.environ["MAILTRAP_PASSWORD"])

    (before, _) = mailbox.stat()

    # Register normally
    response = register({
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
