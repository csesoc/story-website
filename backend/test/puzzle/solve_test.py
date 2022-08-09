import pytest
from common.exceptions import RequestError

# Import for pytest
from test.helpers import clear_all, db_add_user
from test.fixtures import app, client

def test_solve_correct(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    response = client.get("/puzzle/input", json={
        "competition": "2022 Advent of Code",
        "dayNum": 1,
        "part": 1
    })

    data = response.get_json()["input"].split()
    solution = 0
    for num in data:
        solution += int(num)

    response = client.post("/puzzle/solve", json={
        "competition": "2022 Advent of Code",
        "dayNum": 1,
        "part": 1,
        "solution": str(solution)
    })
    assert response.get_json()["correct"] == True