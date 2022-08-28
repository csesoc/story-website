from datetime import timedelta
import os

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from email_validator import validate_email, EmailNotValidError
from itsdangerous import URLSafeTimedSerializer

from common.exceptions import AuthError, InvalidError, RequestError
from common.redis import add_verification, get_verification
from database.user import add_user, email_exists, fetch_user, get_user_info, username_exists

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

verify_serialiser = URLSafeTimedSerializer(os.environ["FLASK_SECRET"], salt="verify")

class User:
    def __init__(self, id, email, username, password, github_username=None):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

        self.github_username = github_username

    # Helper methods

    @staticmethod
    def hash_password(password):
        return hasher.hash(password)

    # API-facing methods

    @staticmethod
    def register(email, username, password):
        """Given an email, username and password, creates a verification code
           for that user in Redis such that we can verify that user's email."""

        # Check for malformed input
        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise RequestError(description="Invalid email") from e

        if email_exists(normalised):
            raise RequestError(description="Email already registered")

        if username_exists(username):
            raise RequestError(description="Username already used")
        
        # Our account is good, we hash the password
        hashed = hasher.hash(password)

        # Add verification code to Redis cache, with expiry date of 1 hour
        code = verify_serialiser.dumps(normalised)

        data = {
            "email": normalised,
            "username": username,
            "password": hashed
        }

        add_verification(data, code)

        return code

    @staticmethod
    def register_verify(code):
        result = get_verification(code)

        if result is None:
            raise AuthError("Token expired or does not correspond to registering user")

        id = add_user(result["email"], result["username"], result["password"])
        return User(id, result["email"], result["username"], result["password"])

    @staticmethod
    def login(email, password):
        """Logs user in with their credentials (currently email and password)."""
        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise AuthError(description="Invalid email or password") from e

        result = fetch_user(normalised)

        try:
            id, email, github_username, username, hashed = result
            hasher.verify(hashed, password)
        except (TypeError, VerificationError) as e:
            raise AuthError(description="Invalid email or password") from e

        return User(id, email, username, hashed, github_username)

    @staticmethod
    def get(id):
        """Given a user's ID, fetches all of their information from the database."""

        result = get_user_info(id)

        if result is None:
            raise InvalidError(description=f"Requested user ID {id} doesn't exist")

        id, email, github_username, username, password = result

        return User(id, email, username, password, github_username)