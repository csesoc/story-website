import email
import os
import poplib
import re

# Imports for pytest
from test.helpers import clear_all, db_add_user,get_cookie_from_response
from test.fixtures import app, client

## HELPER FUNCTIONS

def find_token(contents):
    verify_link = "http://localhost:5001/verify/"
    results = re.findall(rf"<a href=\"{verify_link}(.*?)\">", contents)

    return results[0]

### test starts here

def test_email_request(client):
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

    csrf_token = get_cookie_from_response(response, "csrf_access_token")["csrf_access_token"]
    csrf_headers = {"X-CSRF-TOKEN": csrf_token}

    reset = client.post("/user/reset_email/request", json={
        "email": "numail@gmail.com"
    },headers=csrf_headers)
    
    assert reset.status_code == 200

def test_email_request_invalida_email(client):
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

    csrf_token = get_cookie_from_response(response, "csrf_access_token")["csrf_access_token"]
    csrf_headers = {"X-CSRF-TOKEN": csrf_token}

    reset = client.post("/user/reset_email/request", json={
        "email": "chungas"
    },headers=csrf_headers)
    
    assert reset.status_code == 400
