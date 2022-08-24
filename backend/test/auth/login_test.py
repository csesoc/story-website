from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

# Import for pytest
from flask.testing import FlaskClient
from test.helpers import clear_all, db_add_user, generate_csrf_header
from test.fixtures import app, client


def test_no_users(client):
    clear_all()

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 401


def test_invalid_email(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "foobar@gmail.com",
        "password": "foobaz"
    })

    assert response.status_code == 401


def test_wrong_password(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobaz"
    })

    assert response.status_code == 401

def test_success(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

def test_lockout(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    # Incorrect login 3 times
    for _ in range(3):
        response = client.post("/auth/login", json={
            "email": "asdfghjkl@gmail.com",
            "password": "foobaz"
        })

        assert response.status_code == 401

    # Now when we login, it should lock user out
    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 401

def test_lockout_timing(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    # Incorrect login 3 times
    for _ in range(3):
        response = client.post("/auth/login", json={
            "email": "asdfghjkl@gmail.com",
            "password": "foobaz"
        })

        assert response.status_code == 401

    timeout_over = datetime.now() + timedelta(minutes=1, seconds=5)

    # Incorrect login again
    with freeze_time(timeout_over):
        response = client.post("/auth/login", json={
            "email": "asdfghjkl@gmail.com",
            "password": "foobaz"
        })

        assert response.status_code == 401

    still_timeout = timeout_over + timedelta(minutes=1)

    # Timeout is now 2 minutes
    with freeze_time(still_timeout):
        response = client.post("/auth/login", json={
            "email": "asdfghjkl@gmail.com",
            "password": "foobar"
        })

        assert response.status_code == 401

    second_timeout_over = still_timeout + timedelta(minutes=1, seconds=5)

    # Timeout is now 2 minutes
    with freeze_time(second_timeout_over):
        response = client.post("/auth/login", json={
            "email": "asdfghjkl@gmail.com",
            "password": "foobar"
        })

        assert response.status_code == 200

def test_protected_route(client: FlaskClient):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.post("/auth/protected", headers=generate_csrf_header(response))

    assert response.status_code == 200
