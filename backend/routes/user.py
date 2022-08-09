from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity

import re

from common.exceptions import AuthError, RequestError
from common.database import getCompetitionQuestions, getUserStatsPerComp, updateUsername
from database.user import username_exists
from models.user import User

user = Blueprint("user", __name__)

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



@user.route("/user/stats", methods=['GET'])
def get_stats():

    # Raise RequestError if competition is not valid

    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        competition = request.args.get('competition')
        user_data = User.get(id)


        if getCompetitionQuestions(competition) == {}:
            raise RequestError("The competition doesn't exist")

        stats = getUserStatsPerComp(competition, user_data.id)
        
        ## find a way to get the stat infos, they are spread across multiple tables.

        return jsonify({
            "stats": stats
        })
    except:
        raise AuthError("Invalid token")

@user.route("/user/set_name", methods=['POST'])
def set_name():
    '''
    {
    token: token (in cookies)
    username: string
    }
    '''
    
    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        user_data = User.get(id)
        json = request.get_json()
        username = json["username"]

        # if username already in database, raise RequestError.
        if username_exists(username):
            raise RequestError(description="Username already used")
        else:
            updateUsername(username, id)

        return jsonify({})
    except:
        raise AuthError("Invalid token")

"""
@user.route("/user/reset_email/request", methods=["POST"])
def reset_email_request():
    data = request.get_json()
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


    # Check if email refers to an actual email.
    if not re.match('^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$', data['email']):
        raise RequestError("email not valid")
    return {}



    
@user.route("/user/reset_email/reset", methods=['POST'])
def reset_email():
    json = request.get_json()
    '''
    {
    token: token (in cookie)
    reset_code: string
    }
    '''
    try:
        verify_jwt_in_request()
    except:
        raise AuthError("Invalid token")

    '''
    if (json['reset_code'] not match the code in database for user):
        raise AuthError("The reset code is wrong.")
    else:
        reset email.
    '''



@user.route("/user/reset_password/request", methods=["POST"])
def reset_password_request():
    json = request.get_json()
    return jsonify({})


"""