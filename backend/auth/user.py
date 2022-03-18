from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from email_validator import validate_email, EmailNotValidError

from common.database import get_connection
from common.exceptions import AuthError, InvalidError

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=2**15,
    parallelism=1
)

class User:
    # Private helper methods
    @staticmethod
    def _email_exists(cursor, email):
        cursor.execute("SELECT * FROM users WHERE email = %s",
                       (email,))

        results = cursor.fetchall()
        return results != []

    @staticmethod
    def _add_user(conn, cursor, email, password):
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)",
                       (email, password))
        conn.commit()

        cursor.execute("SELECT uid FROM users WHERE email = %s", (email,))
        id = cursor.fetchone()[0]

        return id

    # Constructor methods
    def __init__(self, email, password, id):
        self.email = email
        self.password = password
        self.id = id

    @staticmethod
    def register(email, password):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise AuthError(description="Invalid email") from e

        if User._email_exists(cursor, normalised):
            raise AuthError(description="Email already registered")
        
        hashed = hasher.hash(password)
        new_id = User._add_user(conn, cursor, normalised, hashed)

        cursor.close()
        conn.close()

        return User(normalised, hashed, new_id)

    @staticmethod
    def login(email, password):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            normalised = validate_email(email).email
        except EmailNotValidError as e:
            raise AuthError(description="Invalid email or password") from e

        cursor.execute("SELECT * FROM users WHERE email = %s", (normalised,))
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
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE uid = %s", (id,))
        fetched = cursor.fetchall()

        if fetched == []:
            raise InvalidError(description=f"Requested user ID {id} doesn't exist")

        email, password, _ = fetched[0]

        cursor.close()
        conn.close()

        return User(email, password, id)
