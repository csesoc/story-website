import os
import psycopg2

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
database = os.environ["POSTGRES_DB"]

TABLES = ["Users", "Questions", "Competitions", "Inputs", "Solves"]

def get_connection():
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

    return conn

def clear_database():
    conn = get_connection()
    cursor = conn.cursor()

    for table in TABLES:
        cursor.execute(f"TRUNCATE TABLE {table} CASCADE")

    conn.commit()

    cursor.close()
    conn.close()
