import pytest

# Import for pytest
from test.helpers import clear_all, db_add_user
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
