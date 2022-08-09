import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity

# what does this do? ask Hanyuan
from puzzles.calendar.calendar import calendar

import re

from common.exceptions import AuthError, RequestError
from common.database import getCompetitionQuestions, getNLeaderboard, searchLeaderboard, getRankLeaderboard
from models.user import User
from itsdangerous import URLSafeTimedSerializer

leaderboard = Blueprint("leaderboard", __name__)
verify_serialiser = URLSafeTimedSerializer(os.environ["FLASK_SECRET"], salt="verify")

@jwt_required()
@leaderboard.route("/entries", methods=['GET'])
def get_leaderboard_twenty():

    # {
    #   token: token (in cookies),
    #   competition: string,
    #   search: string
    # }

    # {
    #   leaderboard: score[]
    # }


    print('hello')
    try:
        print('hello1')
        verify_jwt_in_request()
        print('hello2')

        id = get_jwt_identity()
        competition = request.args.get('competition')
        if getCompetitionQuestions(competition) == {}:
            raise RequestError("The competition doesn't exist")        

        prefix = request.args.get('string')
        returnList = []

        if (prefix is None or prefix == ''):
            print('hello3')

            scores = getNLeaderboard(competition, 20)
            for (idx, score) in enumerate(scores):
                returnList.append({
                  "github": score[0],
                  "username": score[1],
                  "rank": idx + 1,
                  "numStars": score[2],
                  "points": score[3]
                })
        else: 
            scores = searchLeaderboard(competition, prefix, 20)
            for (idx, score) in enumerate(scores):
                returnList.append({
                  "github": score[0],
                  "username": score[1],
                  "rank": idx + 1,
                  "numStars": score[2],
                  "points": score[3]
                })

        ## find a way to get the stat infos, they are spread across multiple tables.

        return jsonify({
            "leaderboard": returnList
        })
    except:
        raise AuthError("Invalid token")

@jwt_required()
@leaderboard.route("/position", methods=['GET'])
def get_leaderboard_position():

    # {
    #   token: token (in cookies),
    #   competition: string
    # }

    # {
    # position: integer
    # }

    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
        competition = request.args.get('competition')
        if getCompetitionQuestions(competition) == {}:
            raise RequestError("The competition doesn't exist")

        return jsonify({
            "position": getRankLeaderboard(competition, id)
        })
    except:
        raise AuthError("Invalid token")