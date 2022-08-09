from common.exceptions import RequestError
import pytest

# Import for pytest
from test.helpers import clear_all, db_add_user
from test.fixtures import app, client

def test_no_competition(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.post("/puzzle/all", params={
        "competition": "Birds can't fly"
    })

    assert response.status_code == RequestError.code


def test_puzzle_all(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.post("/puzzle/all", params={
        "competition": "2022 Advent of Code"
    })

    assert response.status_code == 200
    assert response.json()["puzzles"][0]["dayNum"] == 1
    assert response.json()["puzzles"][0]["part"]["partNum"] == 1

def test_puzzle_no_day(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.post("/puzzle/details", params={
        "competition": "2022 Advent of Code",
        "day": 10000
    })

    assert response.status_code == RequestError.code

def test_puzzle_details(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.post("/puzzle/all", params={
        "competition": "2022 Advent of Code",
        "day": 1
    })

    assert response.status_code == 200