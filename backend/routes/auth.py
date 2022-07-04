import os
from flask import Blueprint, render_template, request, jsonify
from flask_mail import Message
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request

from common.exceptions import AuthError
from common.plugins import mail
from common.redis import cache
from models.user import User

# Constants

auth = Blueprint("auth", __name__)

# Routes (fairly temporary here)
# TODO: update once CSESoc federated auth is set up, do proper research

@auth.route("/login", methods=["POST"])
def login():
    json = request.get_json()

    user = User.login(json["email"], json["password"])
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

@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    response = jsonify({})
    unset_jwt_cookies(response)

    return response, 200
