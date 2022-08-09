from common.database import addCompetition, addReplica
import pytest

# Import for pytest
from test.helpers import clear_all, db_add_user
from test.fixtures import app, client

def test_no_competition(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": ""
    })

    assert response.status_code == 404

def test_no_users_on_leaderboard(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    addCompetition("Alice in Pointerland")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": ""
    })


    assert response.status_code == 200
    assert len(response.json.leaderboard) == 1

def test_one_user_on_leaderboard(client):
    clear_all()

    addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "manavBestie", "zelda", "manavBestie@gmail.com", "noone")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": ""
    })

    assert response.status_code == 200
    assert len(response.json.leaderboard) == 1

def test_two_user_on_leaderboard(client):
    clear_all()

    addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "manavBestie", "zelda", "manavBestie@gmail.com", "noone")
    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": ""
    })

    assert response.status_code == 200
    assert len(response.json.leaderboard) == 2

def test_one_search_on_leaderboard(client):
    clear_all()

    addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "manavBestie", "zelda", "manavBestie@gmail.com", "noone")
    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": "manav"
    })

    assert response.status_code == 200
    assert len(response.json.leaderboard) == 1

def test_many_search_on_leaderboard(client):
    clear_all()

    addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "asdfg", "zelda", "asdfg@gmail.com", "noone")
    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": "asdfg"
    })

    assert response.status_code == 200
    assert len(response.json.leaderboard) == 2

def test_zero_search_on_leaderboard(client):
    clear_all()

    addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "asdfg", "zelda", "asdfg@gmail.com", "noone")
    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": "vanam"
    })

    assert response.status_code == 200
    assert len(response.json.leaderboard) == 0
