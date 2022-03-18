from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies

from auth.user import User

# Constants

auth = Blueprint("auth", __name__)

# Routes

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
    json = request.get_json()
    
    user = User.register(json["email"], json["password"])
    token = create_access_token(identity=user)

    response = jsonify({})
    set_access_cookies(response, token)

    return response, 200

@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    response = jsonify({})
    unset_jwt_cookies(response)

    return response, 200
