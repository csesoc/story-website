from test.helpers import clear_all, db_add_user
from test.fixtures import app, client

def test_success(client):
    clear_all()

    db_add_user("asdfghjkl@gmail.com", "asdf", "foobar")
    
    # Log user in
    login_response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "foobar"
    })

    assert login_response.status_code == 200

    # Log user out
    response = client.post("/auth/logout")

    assert response.status_code == 200

    # Check there's no more cookies
    assert len(client.cookie_jar) == 0
    
