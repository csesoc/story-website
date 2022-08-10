from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity
from flask_mail import Message
from email_validator import validate_email, EmailNotValidError
import re
import os

from datetime import timedelta
from common.exceptions import AuthError, RequestError
from common.database import getCompetitionQuestions, getUserStatsPerComp, updateUsername, updateEmail
from database.user import username_exists
from models.user import User
from itsdangerous import URLSafeTimedSerializer
from common.redis import cache
from common.plugins import mail

user = Blueprint("user", __name__)
verify_serialiser = URLSafeTimedSerializer(os.environ["FLASK_SECRET"], salt="verify")

@jwt_required()
@user.route("/profile", methods=["GET"])
def get_profile():
    try:
        verify_jwt_in_request()
        id = get_jwt_identity()

        user_data = User.get(id)

        return jsonify({
            "email": user_data.email,
            "username": user_data.username
        })
    except:
        raise AuthError("Invalid Token")


@jwt_required()
@user.route("/stats", methods=['GET'])
def get_stats():

    # Raise RequestError if competition is not valid

    try:
        verify_jwt_in_request()
    except:
        raise AuthError("Invalid token")

    id = get_jwt_identity()
    competition = request.args.get('competition')

    if getCompetitionQuestions(competition) == {}:
        raise RequestError("The competition doesn't exist")
    stats = getUserStatsPerComp(competition, id)
    return jsonify({
        "stats": stats
    })

@jwt_required()
@user.route("/set_name", methods=['POST'])
def set_name():
    # {
    # token: token (in cookies)
    # username: string
    # }
    
    try:
        verify_jwt_in_request() # Something is going very wrong with the token and I have no idea what's happening
        id = get_jwt_identity()
    except Exception as e:
        print(e)
        raise AuthError("Invalid token")
    user_data = User.get(id)
    json = request.get_json()
    username = json["username"]

    # if username already in database, raise RequestError.
    if username_exists(username):
        raise RequestError(description="Username already used")
    else:
        updateUsername(username, id)

    return jsonify({})

@jwt_required()
@user.route("/reset_email/request", methods=["POST"])
def reset_email_request():
    json = request.get_json()
    '''
    {
        token: token (in cookies)
        email: string
    }
    '''
    try:
        verify_jwt_in_request()
    except:
        raise AuthError("Invalid token")
    try:
        normalised = validate_email(json['email']).email
    except EmailNotValidError as e:
        raise RequestError(description="Invalid email") from e
    id = get_jwt_identity()
    # user_data = User.get(id)

    code = verify_serialiser.dumps(json["email"])
    data = {
        "email": normalised,
    }

    # We use a pipeline here to ensure these instructions are atomic
    pipeline = cache.pipeline()
    pipeline.hset(f"email_reset_code:{code}", mapping=data)
    pipeline.expire(f"email_reset_code:{code}", timedelta(hours=1))
    pipeline.execute()

    url = f"{os.environ['TESTING_ADDRESS']}/verify/{code}"
    html = render_template("email_request.html", reset_code=url)

    # Send it over to email
    message = Message(
        "Email Request for Week in Wonderland",
        sender="weekinwonderland@csesoc.org.au",
        recipients=[json["email"]],
        html=html
    )

    mail.send(message)

    response = jsonify({})

    return response, 200
    
@user.route("/reset_email/reset", methods=['POST'])
def reset_email():
    json = request.get_json()
    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
    except:
        raise AuthError("Invalid token")

    cache_key = f"email_reset_code:{json['reset_code']}"
    if not cache.exists(cache_key):
        raise AuthError("Reset code expired or does not correspond to registering user")
    result = cache.hgetall(cache_key)
    stringified = {}
    
    for key, value in result.items():
        stringified[key.decode()] = value.decode()
    updateEmail(stringified["email"], id)
    response = jsonify({})
    return response, 200



@user.route("/reset_password/request", methods=["POST"])
def reset_password_request():

    json = request.get_json()
    '''
    {
        token: token (in cookies)
        email: string
    }
    '''
    try:
        verify_jwt_in_request()
    except:
        raise AuthError("Invalid token")

    try:
        normalised = validate_email(json['email']).email
    except EmailNotValidError as e:
        raise RequestError(description="Invalid email") from e

    id = get_jwt_identity()
    # user_data = User.get(id)

    code = verify_serialiser.dumps(json["email"])
    data = {
        "email": normalised,
    }
    # We use a pipeline here to ensure these instructions are atomic
    pipeline = cache.pipeline()
    pipeline.hset(f"password_reset_code:{code}", mapping=data)
    pipeline.expire(f"password_reset_code:{code}", timedelta(hours=1))
    pipeline.execute()

    url = f"{os.environ['TESTING_ADDRESS']}/verify/{code}"
    html = render_template("email_request.html", reset_code=url)

    # Send it over to email
    message = Message(
        "Email Request for Week in Wonderland",
        sender="weekinwonderland@csesoc.org.au",
        recipients=[json["email"]],
        html=html
    )

    mail.send(message)
    response = jsonify({})
    return response, 200
