import email
import os
import poplib
import re
from sqlite3 import paramstyle

# Imports for pytest
from test.helpers import clear_all
from test.fixtures import app, client

## HELPER FUNCTIONS

def find_token(contents):
    verify_link = "http://localhost:5001/verify/"
    results = re.findall(rf"<a href=\"{verify_link}(.*?)\">", contents)

    return results[0]

### test starts here

def test_stats(client):
    clear_all()

    register_response = client.post("/auth/register", json={
        "email": "asdfghjkl@gmail.com",
        "username": "asdf",
        "password": "foobar"
    })

    assert register_response.status_code == 200

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

    response = client.post("/auth/register/verify", json={
        "token": token
    })

    assert response.status_code == 200
    profile = client.get("/user/profile")
    assert profile.status_code == 200
    assert profile.json == {
        "email": "asdfghjkl@gmail.com",
        "username": "asdf"
    }
    # , params={'competition': 'Alice in Wonderweek'}
    stats = client.get("/user/stats", json={
        "competition": 'Alice in Wonderweek'
    }) 
    assert stats.status_code == 200

