import os
from flask import Blueprint, render_template, request, jsonify
from flask_mail import Message
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request

from common.exceptions import AuthError
from common.plugins import mail
from common.redis import block, calculate_time, incorrect_attempts, is_blocked, register_incorrect
from database.user import fetch_id
from models.user import User

# Constants

auth = Blueprint("auth", __name__)

# Routes (fairly temporary here)

@auth.route("/login", methods=["POST"])
def login():
    json = request.get_json()

    id = fetch_id(json["email"])

    if is_blocked(id):
        raise AuthError()

    try:
        user = User.login(json["email"], json["password"])
    except Exception as e:
        register_incorrect(id)

        attempts = incorrect_attempts(id)

        if attempts >= 3:
            block_time = calculate_time(attempts)
            block(id, block_time)

        raise e

    token = create_access_token(identity=user)

    response = jsonify({})
    set_access_cookies(response, token)

    return response, 200

@auth.route("/register", methods=["POST"])
def register():
    # TODO: convert to email verification once we get email address
    json = request.get_json()
    
    # Fetch verification code
    code = User.register(json["email"], json["username"], json["password"])

    # jason - temporarily don't do verification for testing frontend fetches
    # User.register_verify(code)
    # return jsonify({}), 200

    # TODO: convert to domain of verification page once we have its address
    url = f"{os.environ['TESTING_ADDRESS']}/verify/{code}"

    html = render_template("activate.html", confirm_url=url)

    # Send it over to email
    message = Message(
        "Account registered for Week in Wonderland",
        sender="weekinwonderland@csesoc.org.au",
        recipients=[json["email"]],
        html=html
    )

    mail.send(message)

    response = jsonify({})

    return response, 200

@auth.route("/register/verify", methods=["POST"])
def register_verify():
    json = request.get_json()

    user = User.register_verify(json["token"])
    cookie = create_access_token(identity=user)

    response = jsonify({})
    set_access_cookies(response, cookie)

    return response, 200

@auth.route("/verify_token", methods=["GET"])
def verify_token():
    try:
        verify_jwt_in_request()
    except:
        raise AuthError("Not logged in")

    return jsonify({}), 200

@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify({})
    unset_jwt_cookies(response)

    return response, 200

@jwt_required()
@auth.route("/protected", methods=["POST"])
def protected():
    verify_jwt_in_request()
    return jsonify({}), 200