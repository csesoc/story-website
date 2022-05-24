from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from email_validator import validate_email, EmailNotValidError

from common.database import get_connection
from common.exceptions import AuthError, InvalidError, RequestError

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

class User:
    # Private helper methods
    @staticmethod
    def _email_exists(cursor, email):
        """Checks if an email exists in the database."""
        cursor.execute("SELECT * FROM Users WHERE email = %s",
                       (email,))

        results = cursor.fetchall()
        return results != []

    @staticmethod
    def _add_user(conn, cursor, email, username, password):
        """Given the details of a user, adds them to the database."""
        cursor.execute("INSERT INTO Users (email, username, password, numStars, score) VALUES (%s, %s, %s, 0, 0)",
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

    @staticmethod
    def register(email, username, password):
        # TODO: update register function once we get custom email
        """Given an email, username and password, registers the user in the
           database."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise RequestError(description="Invalid email") from e

        if User._email_exists(cursor, normalised):
            raise RequestError(description="Email already registered")
        
        hashed = hasher.hash(password)
        new_id = User._add_user(conn, cursor, normalised, username, hashed)

        cursor.close()
        conn.close()

        return User(normalised, hashed, new_id)

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
        # TODO: update with new DB schema
        """Given a user's ID, fetches all of their information from the database."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE uid = %s", (id,))
        fetched = cursor.fetchall()

        if fetched == []:
            raise InvalidError(description=f"Requested user ID {id} doesn't exist")

        email, password, _ = fetched[0]

        cursor.close()
        conn.close()

        return User(email, password, id)
