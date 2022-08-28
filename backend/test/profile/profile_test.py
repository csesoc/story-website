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

def test_profile(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")
    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })
    assert response.status_code == 200
    
    profile2 = client.get("/user/profile", headers=generate_csrf_header(response))
    assert profile2.status_code == 200
    assert profile2.json == {
        "email": "asdfghjkl@gmail.com",
        "username": "asdf"
    }

def test_profile_fail(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    profile2 = client.get("/user/profile")
    assert profile2.status_code == 401

