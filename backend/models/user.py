from datetime import timedelta
import os

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from email_validator import validate_email, EmailNotValidError
from itsdangerous import URLSafeTimedSerializer

from common.exceptions import AuthError, InvalidError, RequestError
from common.redis import cache
from database.database import db
from database.user import add_user, email_exists, fetch_user, username_exists

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

verify_serialiser = URLSafeTimedSerializer(os.environ["FLASK_SECRET"], salt="verify")

class User:
    def __init__(self, id, email, username, password, stars=0, score=0):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.stars = stars
        self.score = score

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

        # We use a pipeline here to ensure these instructions are atomic
        pipeline = cache.pipeline()

        pipeline.hset(f"register:{code}", mapping=data)
        pipeline.expire(f"register:{code}", timedelta(hours=1))

        pipeline.execute()

        return code

    @staticmethod
    def register_verify(token):
        cache_key = f"register:{token}"

        if not cache.exists(cache_key):
            raise AuthError("Token expired or does not correspond to registering user")

        result = cache.hgetall(cache_key)
        stringified = {}
        
        for key, value in result.items():
            stringified[key.decode()] = value.decode()

        id = add_user(stringified["email"], stringified["username"], stringified["password"], 0, 0)
        return User(id, stringified["email"], stringified["username"], stringified["password"])

    @staticmethod
    def login(email, password):
        """Logs user in with their credentials (currently email and password)."""
        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise AuthError(description="Invalid email or password") from e

        result = fetch_user(normalised)

        try:
            id, email, username, stars, score, hashed = result
            hasher.verify(hashed, password)
        except (TypeError, VerificationError) as e:
            raise AuthError(description="Invalid email or password") from e

        return User(id, email, username, hashed, stars, score)

    @staticmethod
    def get(id):
        """Given a user's ID, fetches all of their information from the database."""
        conn = db.getconn()

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE uid = %s", (id,))
            fetched = cursor.fetchall()

            if fetched == []:
                raise InvalidError(description=f"Requested user ID {id} doesn't exist")

            id, email, username, stars, score, password = fetched[0]

        db.putconn(conn)

        return User(id, email, username, password, stars, score)
