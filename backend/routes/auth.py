from flask import Blueprint, request

from database import get_connection

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    pass

@auth.route("/register", methods=["POST"])
def register():
    response = request.get_json()
    
    conn = get_connection()
    cursor = conn.cursor()

    # TODO: hash passwords
    cursor.execute("INSERT INTO users (email, password)"
                   "VALUES (%s, %s)",
                   (response["email"], response["password"]))
    conn.commit()

    cursor.close()
    conn.close()

    return "{}"
