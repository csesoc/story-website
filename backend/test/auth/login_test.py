import os
import requests

from database.user import add_user
from models.user import User
# Import for pytest
from test.helpers import clear_all
from test.fixtures import app, client

def db_add_user(email, username, password):
    add_user(email, username, User.hash_password(password), 0, 0)

def login(json):
    response = requests.post(f"{os.environ['TESTING_ADDRESS']}/auth/login", json=json)
    return response

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
