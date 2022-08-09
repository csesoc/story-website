import os
from psycopg2.pool import ThreadedConnectionPool

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
database = os.environ["POSTGRES_DB"]

# TABLES = ["Users", "Questions", "Parts", "Competitions", "Inputs", "Solves"]

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
        cursor.execute(f"""SELECT truncate_tables();""")
        conn.commit()
    
    db.putconn(conn)

