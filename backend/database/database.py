import os
from psycopg2.pool import ThreadedConnectionPool

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
database = os.environ["POSTGRES_DB"]

db = ThreadedConnectionPool(
    1, 20,
    user=user,
    password=password,
    host=host,
    port=port,
    database=database
)

def clear_database():
    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")

        for table in cursor.fetchall():
            cursor.execute(f"TRUNCATE TABLE {table[0]} CASCADE")

        conn.commit()
    
    db.putconn(conn)
