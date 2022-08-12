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

def test_password_reset(client):
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
        "email": "numail@gmail.com"
    },headers=generate_csrf_header(response))
    
    assert reset.status_code == 200

    # Check inbox
    mailbox = poplib.POP3("pop3.mailtrap.io", 1100)
    mailbox.user(os.environ["MAILTRAP_USERNAME"])
    mailbox.pass_(os.environ["MAILTRAP_PASSWORD"])

    # Check the contents of the email, and harvest the token from there
    raw_email = b"\n".join(mailbox.retr(1)[1])
    parsed_email = email.message_from_bytes(raw_email)

    # Assuming there's a HTML part
    for part in parsed_email.walk():
        if part.get_content_type() == "text/html":
            content = part.get_payload()

    # Extract the token from the HTML
    token = find_token(content)

    response = client.post("/user/reset_password/reset", json={
        "reset_code": token,
        "password": "ghjkl"
    })

    assert response.status_code == 200

    response = client.post("/auth/logout")

    assert response.status_code == 200

    # Check there's no more cookies
    assert len(client.cookie_jar) == 0

    response = client.post("/auth/login", json={
        "email": "asdfghjkl@gmail.com",
        "password": "ghjkl"
    })
    
    assert response.status_code == 200
