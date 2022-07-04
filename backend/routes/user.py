from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity

import re

from common.exceptions import AuthError, RequestError
from common.database import get_connection
from auth.user import User

user = Blueprint("user", __name__)

@user.route("/profile", methods=["GET"])
@jwt_required
def get_profile():
    try:
        id = get_jwt_identity()

        user_data = User.get(id)

        return {
            "email": user_data.email,
            "username": username
        }
    except:
        raise AuthError("Invalid Token")



@user.route("/user/stats", methods=['GET'])
def get_stats():
    token = request.args.get('token')
    competition = request.args.get('competition')

    # Raise RequestError if competition is not valid ()

    try:
        header, content = verify_jwt_in_request()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM Competitions WHERE uid = %s", (content['id']))
        competition = cursor.fetchone()[0]
        if competition is "":
            raise RequestError
        
        ## find a way to get the stat infos, they are spread across multiple tables.

        return {
            "stats": []
        }
    except:
        raise AuthError("Invalid token")


@user.route("/user/set_name", methods=['POST'])
def set_name():
    json = request.get_json()
    '''
    {
    token: token (in cookies)
    username: string
    }
    '''
    # if username already in database, raise RequestError.
    try:
        verify_jwt_in_request()
        return {}
    except:
        raise AuthError("Invalid token")

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


