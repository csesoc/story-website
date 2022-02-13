from argon2 import PasswordHasher
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, request

from common.database import get_connection
from common.exceptions import AuthError

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    pass

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

    # TODO: check if email is already in database or not

    # Hash password
    hashed = hasher.hash(response["password"])

    cursor.execute("INSERT INTO users (email, password)"
                   "VALUES (%s, %s)",
                   (normalised.email, hashed))
    conn.commit()

    cursor.close()
    conn.close()

    return "{}"
