import pytest

# Import for pytest
from test.helpers import clear_all, db_add_user
from test.fixtures import app, client


# Example test

# def test_no_users(client):
#     clear_all()

#     response = client.post("/auth/login", json={
#         "email": "asdfghjkl@gmail.com",
#         "password": "foobar"
#     })

#     assert response.status_code == 401

