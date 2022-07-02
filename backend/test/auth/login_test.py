import os
import requests

from database.database import clear_database
# Used for testing purposes!
from database.user import add_user
from models.user import User

def testing_add_user(email, username, password):
    user = User(email, username, User.hash_password(password))
    add_user(*user.to_tuple())

def login(json):
    response = requests.post(f"{os.environ['TESTING_ADDRESS']}/auth/login", json=json)
    return response

def test_no_users():
    clear_database()

    response = login({
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert response.status_code == 400

def test_invalid_email():
    clear_database()

    testing_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = login({
        "email": "foobar@gmail.com",
        "password": "foobaz"
    })

    assert response.status_code == 400

def test_wrong_password():
    clear_database()

    testing_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = login({
        "email": "asdfghjkl@gmail.com",
        "password": "foobaz"
    })

    assert response.status_code == 400

def test_success():
    clear_database()

    testing_add_user("asdfghjkl@gmail.com", "asdf", "foobar")

    response = login({
        ""
    })
