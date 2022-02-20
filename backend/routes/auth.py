from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, request

from common.database import get_connection
from common.exceptions import AuthError

# Constants

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

auth = Blueprint("auth", __name__)

# Helper functions

def email_exists(cursor, email):
    cursor.execute("SELECT * FROM users WHERE email = %s",
                   (email,))

    results = cursor.fetchall()
    return results != []

# Routes

@auth.route("/login", methods=["POST"])
def login():
    response = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    # Verify email provided is a valid address
    try:
        normalised = validate_email(response["email"])
    except EmailNotValidError as e:
        raise AuthError(description="Invalid email") from e

    # Check if email is already in database or not
    if not email_exists(cursor, normalised.email):
        raise AuthError(description="Email or password is incorrect")

    cursor.execute("SELECT password FROM users WHERE email = %s",
                   (normalised.email,))
    db_password = cursor.fetchone()[0]

    # Incorrect password
    try:
        hasher.verify(db_password, response["password"])
    except VerifyMismatchError as e:
        raise AuthError(description="Email or password is incorrect") from e

    cursor.close()
    conn.close()

    # TODO: return a proper success message
    return "{}"

@auth.route("/register", methods=["POST"])
def register():
    response = request.get_json()
    
    conn = get_connection()
    cursor = conn.cursor()

    # Verify email provided is a valid address
    try:
        normalised = validate_email(response["email"])
    except EmailNotValidError as e:
        raise AuthError(description="Invalid email") from e

    # Check if email is already in database or not
    if email_exists(cursor, normalised.email):
        raise AuthError(description="Email already registered")

    # Hash password
    hashed = hasher.hash(response["password"])

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)",
                   (normalised.email, hashed))
    conn.commit()

    cursor.close()
    conn.close()

    # TODO: return a proper success message
    return "{}"
