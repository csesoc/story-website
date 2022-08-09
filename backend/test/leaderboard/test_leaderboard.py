from common.database import addCompetition, addReplica, addSolve, addUser
from common.exceptions import RequestError
import pytest
import re
import email
import os
import poplib

# Import for pytest
from test.helpers import clear_all, db_add_user
from test.fixtures import app, client

## HELPER FUNCTIONS

def find_token(contents):
    verify_link = "http://localhost:5001/verify/"
    results = re.findall(rf"<a href=\"{verify_link}(.*?)\">", contents)

    return results[0]

# TODO: note that this works only if the mail client works

def test_no_competition(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 200

    response = client.get("/leaderboard/entries", json={
        "competition": "Alice in Pointerland",
        "search": ""
    })

    assert response.status_code == 401

# def test_no_users_on_leaderboard(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addCompetition("Alice in Pointerland")

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": ""
#     })

#     assert response.status_code == 200
#     assert len(response.json.leaderboard) == 1

# def test_one_user_on_leaderboard(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "manavBestie", "zelda", "manavBestie@gmail.com", "noone")

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": ""
#     })

#     assert response.status_code == 200
#     assert len(response.json.leaderboard) == 1

# def test_two_user_on_leaderboard(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "manavBestie", "zelda", "manavBestie@gmail.com", "noone")

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": ""
#     })

#     assert response.status_code == 200
#     assert len(response.json.leaderboard) == 2

# def test_one_search_on_leaderboard(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "manavBestie", "zelda", "manavBestie@gmail.com", "noone")

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": "manav"
#     })

#     assert response.status_code == 200
#     assert len(response.json.leaderboard) == 1

# def test_many_search_on_leaderboard(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200
#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "asdfg", "zelda", "asdfg@gmail.com", "noone")

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": "asdfg"
#     })

#     assert response.status_code == 200
#     assert len(response.json.leaderboard) == 2

# def test_zero_search_on_leaderboard(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "asdfg", "zelda", "asdfg@gmail.com", "noone")

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": "vanam"
#     })

#     assert response.status_code == 200
#     assert len(response.json.leaderboard) == 0

# def test_correct_order_on_leaderboardA(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "asdfg", "zelda", "asdfg@gmail.com", "noone")
#     addSolve(42, 1, 1000, 99)

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": "vanam"
#     })

#     assert response.status_code == 200
#     assert (response.json.leaderboard[0]).username == "asdfg"

#     response = client.get("/leaderboard/position", json={
#         "competition": "Alice in Pointerland"
#     })

#     assert response.status_code == 200
#     assert response.json.position == 1

# def test_correct_order_on_leaderboardB(client):
#     clear_all()

#     db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 200

#     addReplica("Alice in Pointerland", "IMC Banner I", 1, "good luck for trials", "asdfg", "zelda", "asdfg@gmail.com", "noone")
#     addSolve(42, 1, 1000, 101)

#     response = client.get("/leaderboard/entries", json={
#         "competition": "Alice in Pointerland",
#         "search": "vanam"
#     })

#     assert response.status_code == 200
#     assert (response.json.leaderboard[0]).username == "asdf"

#     response = client.get("/leaderboard/position", json={
#         "competition": "Alice in Pointerland"
#     })

#     assert response.status_code == 200
#     assert response.json.position == 2
