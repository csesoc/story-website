import os
import psycopg2

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
database = os.environ["POSTGRES_DB"]

def get_connection():
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

    return conn
