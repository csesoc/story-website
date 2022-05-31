import requests

from auth.user import User
from common.database import get_connection, clear_database

def register(json):
    response = requests.post("http://localhost:5001/auth/register", json=json)
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
    conn = get_connection()
    cursor = conn.cursor()

    User._add_user(conn, cursor, reused_address, "foo", "bar")

    response = register({
        "email": reused_address,
        "username": "foo",
        "password": "bar"
    })

    cursor.close()
    conn.close()

    assert response.status_code == 400

def test_duplicate_username():
    clear_database()

    reused_username = "foo"

    # Register the user in the database directly
    conn = get_connection()
    cursor = conn.cursor()

    User._add_user(conn, cursor, "asdfghjkl@gmail.com", reused_username, "bar")

    response = register({
        "email": "foobar@gmail.com",
        "username": reused_username,
        "password": "bar"
    })

    cursor.close()
    conn.close()

    assert response.status_code == 400

def test_success():
    pass
