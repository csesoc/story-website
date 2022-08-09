from database.database import db


def add_user(email, username, password) -> int:
    """Adds a user to the database, returning their ID."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO Users (email, username, password) VALUES ('{email}', '{username}', '{password}')")
        conn.commit()

        cursor.execute(f"SELECT uid FROM Users WHERE email = '{email}'")
        id = cursor.fetchone()[0]

    db.putconn(conn)
    return id


def fetch_user(email: str):
    """Given a user's email, fetches their content from the database."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM Users WHERE email = '{email}'")
        result = cursor.fetchone()

    db.putconn(conn)
    return result


def email_exists(email: str) -> bool:
    """Checks if an email exists in the users table."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM Users WHERE email = '{email}'")
        results = cursor.fetchall()

    db.putconn(conn)
    return results != []


def username_exists(username: str) -> bool:
    """Checks if a username is already used."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM Users WHERE username = '{username}'")
        results = cursor.fetchall()

    db.putconn(conn)
    return results != []
