import email
import os
import poplib
import re

# Imports for pytest
from test.helpers import clear_all, db_add_user, generate_csrf_header
from test.fixtures import app, client

## HELPER FUNCTIONS

def find_token(contents):
    verify_link = "http://localhost:5001/verify/"
    results = re.findall(rf"<a href=\"{verify_link}(.*?)\">", contents)

    return results[0]

### test starts here

def test_password_test(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })
    assert response.status_code == 200

    profile = client.get("/user/profile")
    assert profile.status_code == 200
    assert profile.json == {
        "email": "asdfghjkl@gmail.com",
        "username": "asdf"
    }

    reset = client.post("/user/reset_password/request", json={
    },headers=generate_csrf_header(response))
    
    assert reset.status_code == 200

def test_password_request_invalid_token(client):
    pass