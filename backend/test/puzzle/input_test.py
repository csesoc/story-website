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

    response = client.get("/puzzle/input", json={
        "competition": "2022 Advent of Code",
        "dayNum": 1,
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

    response1 = client.get("/puzzle/input", json={
        "competition": "2022 Advent of Code",
        "dayNum": 1,
        "part": 1
    })

    db_add_user("user2@gmail.com", "yay", "passss")

    response = client.post("/auth/login", json={
        "email": "user2@gmail.com",
        "password": "passss"
    })

    response2 = client.get("/puzzle/input", json={
        "competition": "2022 Advent of Code",
        "dayNum": 1,
        "part": 1
    })

    assert response1.get_json()["input"] != response2.get_json()["input"]