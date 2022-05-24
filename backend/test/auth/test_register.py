import pytest
import requests

def test_invalid_email():
    # Frontend should detect whether an email address doesn't follow a
    # specific format!
    invalid_address = "foo@guaranteed.invalid"

    response = requests.post("http://localhost:5001/auth/register", json={
        "email": invalid_address,
        "username": "Test",
        "password": "foobar123"
    })

    print(response)

def test_duplicate_email():
    pass

def test_duplicate_username():
    pass

def test_success():
    pass
