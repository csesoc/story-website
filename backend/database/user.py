from database.database import db

# Get all the information about a user given their uid
# Returns all information in the form of a dictionary
def get_user_info(uid):
    conn = db.getconn()

    with conn.cursor() as cursor:
        query = f"""
            select * from Users where uid = {uid};
        """
        cursor.execute(query)

        # only one entry should be returned since day number is unique
        t = cursor.fetchone()

    db.putconn(conn)
    return t


def add_user(email, username, password) -> int:
    """Adds a user to the database, returning their ID."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Users (email, username, password) VALUES (%s, %s, %s)",
                       (email, username, password))
        conn.commit()

        cursor.execute("SELECT uid FROM Users WHERE email = %s", (email,))
        id = cursor.fetchone()[0]

    db.putconn(conn)
    return id


def fetch_id(email: str):
    """Given a user's email, fetches their ID."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("SELECT uid FROM Users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is None:
            db.putconn(conn)
            return None

        id = cursor.fetchone()[0]

    db.putconn(conn)
    return id


def fetch_user(email: str):
    """Given a user's email, fetches their content from the database."""

    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        result = cursor.fetchone()

    db.putconn(conn)
    return result


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
