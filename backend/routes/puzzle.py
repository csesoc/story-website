from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity

from puzzles.calendar.calendar import calendar

import re

from common.exceptions import AuthError, RequestError
from common.database import getCompetitionQuestions, getUserStatsPerComp, updateUsername
from database.user import username_exists
from models.user import User

puzzle = Blueprint("puzzle", __name__)

# @puzzle.route("/description", methods=["GET"])
# def description():
#     year = int(request.args.get("year"))
#     day = int(request.args.get("day"))
#     task = calendar[year][day](0)

#     return jsonify({
#         "description": task.description()
#     })

@puzzle.route("/all", methods=['GET'])
def get_all_puzzles():

    # {
    # token: token (in cookies),
    # competition: string,
    # day: integer
    # }

    # {
    # puzzles : puzzle[]
    # }

    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        pass
    except:
        raise AuthError("Invalid token")

@puzzle.route("/details", methods=['GET'])
def get_puzzle_details():

    # {
    # token: token (in cookies),
    # competition: string,
    # day: integer
    # }

    # {
    # n_parts: integer,
    # name: string,
    # dayNum: integer,
    # parts: part[]
    # }

    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        pass
    except:
        raise AuthError("Invalid token")

@puzzle.route("/all", methods=['GET'])
def get_puzzle_input():

    # {
    # token: token (in cookies),
    # competition: string,
    # day: integer
    # }

    # {
    #   input: string
    # }

    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        pass
    except:
        raise AuthError("Invalid token")

@puzzle.route("/all", methods=['POST'])
def solve_puzzle():

    # {
    # token: token (in cookies),
    # competition: string,
    # day: integer,
    # part: integer,
    # solution: string
    # }

    # {
    # correct: boolean,
    # reason: string
    # }


    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        pass
    except:
        raise AuthError("Invalid token")



# example functions ############################################################################################

# @user.route("/stats", methods=['GET'])
# def get_stats():

#     # Raise RequestError if competition is not valid

#     try:
#         verify_jwt_in_request()
#         id = get_jwt_identity()
#         competition = request.args.get('competition')

#         if getCompetitionQuestions(competition) == {}:
#             raise RequestError("The competition doesn't exist")

#         stats = getUserStatsPerComp(competition, id)
        
#         ## find a way to get the stat infos, they are spread across multiple tables.

#         return jsonify({
#             "stats": stats
#         })
#     except:
#         raise AuthError("Invalid token")

# @user.route("/set_name", methods=['POST'])
# def set_name():
#     '''
#     {
#     token: token (in cookies)
#     username: string
#     }
#     '''
    
#     try:
#         print('hello')
#         print('hello0')
#         verify_jwt_in_request()
#         print('hello1')
#         id = get_jwt_identity()
#         print('hello2')
#         user_data = User.get(id)
#         print('hello3')
#         json = request.get_json()
#         print('hello4')
#         username = json["username"]
#         print('hello5')

#         # if username already in database, raise RequestError.
#         if username_exists(username):
#             raise RequestError(description="Username already used")
#         else:
#             updateUsername(username, id)

#         return jsonify({})
#     except:
#         raise AuthError("Invalid token")