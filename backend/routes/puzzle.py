from inspect import ArgSpec
from xml.sax.handler import all_properties
from common.exceptions import RequestError, AuthError
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from puzzles.calendar.calendar import calendar

puzzle = Blueprint("puzzle", __name__)

def getID():
    try:
        verify_jwt_in_request()
        id = get_jwt_identity()
    except:
        raise AuthError("Invalid token")

    return id


@puzzle.route("/description", methods=["GET"])
def description():
    year = int(request.args.get("year"))
    day = int(request.args.get("day"))
    task = calendar[year][day](0)

    return jsonify({
        "description": task.description()
    })

@jwt_required()
@puzzle.route("/all", methods=["GET"])
def puzzle_all():
    id = getID()

    competition = request.args.get("competitions")
    try:
        days = calendar[competition]
    except:
        raise RequestError("This competition does not exist")

    all_puzzles = []

    for day in days:
        new = day(id)
        all_puzzles.append(new.description())
    return jsonify({
        "puzzles": all_puzzles
    })

@jwt_required()
@puzzle.route("/details", methods=["GET"])
def puzzle_details():
    id = getID()
    competition = str(request.args.get("competitions"))
    dayNum = int(request.args.get("dayNum"))

    try:
        days = calendar[competition]
    except:
        raise RequestError("This competition does not exist")


    try:
        day = days[dayNum - 1]
    except:
        raise RequestError("This day does not exist")

    return jsonify(
        day(id).description() #changed outut structure a bit
    )

@jwt_required()
@puzzle.route("/input", methods=["GET"])
def puzzle_input():
    id = getID()

    competition = str(request.args.get("competitions"))
    dayNum = int(request.args.get("dayNum"))
    part = int(request.args.get("part"))

    try:
        days = calendar[competition]
    except:
        raise RequestError("This competition does not exist")


    try:
        day = days[dayNum - 1]
    except:
        raise RequestError("This day does not exist")

    return jsonify({
        "input": day(id).generate_input(part)
    })

@jwt_required()
@puzzle.route("/solve", methods=["POST"])
def puzzle_solve():
    id = getID()
    competition = str(request.get_json()["competition"])
    dayNum = int(request.get_json()["dayNum"])
    part = str(request.get_json()["part"]) #assume this will be there
    solution = int(request.get_json()["solution"])

    try:
        days = calendar[competition]
    except:
        raise RequestError("This competition does not exist")


    try:
        day = days[dayNum - 1]
    except:
        raise RequestError("This day does not exist")

    return jsonify(day(id).verify(solution, part))

# puzzle = Blueprint("puzzle", __name__)

# # @puzzle.route("/description", methods=["GET"])
# # def description():
# #     year = int(request.args.get("year"))
# #     day = int(request.args.get("day"))
# #     task = calendar[year][day](0)

# #     return jsonify({
# #         "description": task.description()
# #     })

# @puzzle.route("/all", methods=['GET'])
# def get_all_puzzles():

#     # {
#     # token: token (in cookies),
#     # competition: string,
#     # day: integer
#     # }

#     # {
#     # puzzles : puzzle[]
#     # }

#     try:
#         verify_jwt_in_request()
#         id = get_jwt_identity()
#         pass
#     except:
#         raise AuthError("Invalid token")

# @puzzle.route("/details", methods=['GET'])
# def get_puzzle_details():

#     # {
#     # token: token (in cookies),
#     # competition: string,
#     # day: integer
#     # }

#     # {
#     # n_parts: integer,
#     # name: string,
#     # dayNum: integer,
#     # parts: part[]
#     # }

#     try:
#         verify_jwt_in_request()
#         id = get_jwt_identity()
#         pass
#     except:
#         raise AuthError("Invalid token")

# @puzzle.route("/all", methods=['GET'])
# def get_puzzle_input():

#     # {
#     # token: token (in cookies),
#     # competition: string,
#     # day: integer
#     # }

#     # {
#     #   input: string
#     # }

#     try:
#         verify_jwt_in_request()
#         id = get_jwt_identity()
#         pass
#     except:
#         raise AuthError("Invalid token")

# @puzzle.route("/all", methods=['POST'])
# def solve_puzzle():

#     # {
#     # token: token (in cookies),
#     # competition: string,
#     # day: integer,
#     # part: integer,
#     # solution: string
#     # }

#     # {
#     # correct: boolean,
#     # reason: string
#     # }


#     try:
#         verify_jwt_in_request()
#         id = get_jwt_identity()
#         pass
#     except:
#         raise AuthError("Invalid token")



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
