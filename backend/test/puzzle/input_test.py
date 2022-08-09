import pytest
from common.exceptions import RequestError

# Import for pytest
from test.helpers import clear_all, db_add_user
from test.fixtures import app, client

def test_no_part(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.post("/puzzle/input", params={
        "competition": "2022 Advent of Code",
        "day": 1,
        "part": 10000
    })

    assert response.status_code == RequestError.code

def test_unique_input(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    response1 = client.post("/puzzle/input", params={
        "competition": "2022 Advent of Code",
        "day": 1,
        "part": 1
    })

    db_add_user("user2@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "user2@gmail.com",
        "password": "foobar"
    })

    response2 = client.post("/puzzle/input", params={
        "competition": "2022 Advent of Code",
        "day": 1,
        "part": 1
    })

    assert response1.json()["input"] != response2.json()["input"]