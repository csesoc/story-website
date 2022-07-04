from database.database import db


def add_user(email, username, password, stars, score) -> int:
    """Adds a user to the database, returning their ID."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Users (email, username, password, numStars, score) VALUES (%s, %s, %s, %s, %s)",
                       (email, username, password, stars, score))
        conn.commit()

        cursor.execute("SELECT uid FROM Users WHERE email = %s", (email,))
        id = cursor.fetchone()[0]

    db.putconn(conn)
    return id


def email_exists(email: str) -> bool:
    """Checks if an email exists in the users table."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        results = cursor.fetchall()

    db.putconn(conn)
    return results != []


def username_exists(username: str) -> bool:
    """Checks if a username is already used."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        results = cursor.fetchall()

    db.putconn(conn)
    return results != []
