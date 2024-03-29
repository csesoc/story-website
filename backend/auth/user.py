from datetime import timedelta
import random

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from email_validator import validate_email, EmailNotValidError

from common.database import get_connection
from common.exceptions import AuthError, InvalidError, RequestError
from common.redis import cache

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

class User:
    # TODO: change all these functions once database functions are merged

    # Private helper methods
    @staticmethod
    def _email_exists(cursor, email):
        """Checks if an email exists in the database."""
        cursor.execute("SELECT * FROM Users WHERE email = %s",
                       (email,))

        results = cursor.fetchall()
        return results != []

    @staticmethod
    def _username_exists(cursor, username):
        """Checks if a username is already used."""
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))

        results = cursor.fetchall()
        return results != []

    @staticmethod
    def _add_user(conn, cursor, email, username, password):
        """Given the details of a user, adds them to the database."""
        cursor.execute("INSERT INTO Users (email, username, password) VALUES (%s, %s, %s, 0, 0)",
                       (email, username, password))
        conn.commit()

        cursor.execute("SELECT uid FROM Users WHERE email = %s", (email,))
        id = cursor.fetchone()[0]

        return id

    # Constructor methods
    def __init__(self, email, password, id):
        self.email = email
        self.password = password
        self.id = id

    # API-facing methods
    @staticmethod
    def register(email, username, password):
        """Given an email, username and password, creates a verification code
           for that user in Redis such that we can verify that user's email."""
        # Error handling
        conn = get_connection()
        cursor = conn.cursor()

        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise RequestError(description="Invalid email") from e

        if User._email_exists(cursor, normalised):
            raise RequestError(description="Email already registered")

        if User._username_exists(cursor, username):
            raise RequestError(description="Username already used")
        
        hashed = hasher.hash(password)
        # TODO: remove addition of user to database
        new_id = User._add_user(conn, cursor, normalised, username, hashed)

        cursor.close()
        conn.close()

        # Add verification code to Redis cache, with expiry date of 1 hour
        code = random.randint(0, 999_999)
        data = {
            "code": f"{code:06}",
            "username": username,
            "password": hashed
        }

        pipeline = cache.pipeline()

        # We use a pipeline here to ensure these instructions are atomic
        pipeline.hset(f"register:{new_id}", mapping=data)
        pipeline.expire(f"register:{new_id}", timedelta(hours=1))

        pipeline.execute()

        return code

    @staticmethod
    def login(email, password):
        """Logs user in with their credentials (currently email and password)."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise AuthError(description="Invalid email or password") from e

        cursor.execute("SELECT * FROM Users WHERE email = %s", (normalised,))
        result = cursor.fetchone()

        try:
            id, _, hashed = result
            hasher.verify(hashed, password)
        except (TypeError, VerificationError) as e:
            raise AuthError(description="Invalid email or password") from e

        cursor.close()
        conn.close()

        return User(normalised, hashed, id)

    @staticmethod
    def get(id):
        """Given a user's ID, fetches all of their information from the database."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE uid = %s", (id,))
        fetched = cursor.fetchall()

        if fetched == []:
            raise InvalidError(description=f"Requested user ID {id} doesn't exist")

        email, _, password, _, _ = fetched[0]

        cursor.close()
        conn.close()

        return User(email, password, id)