from xml.sax.handler import all_properties
from common.exceptions import RequestError
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from puzzles.calendar.calendar import calendar

puzzle = Blueprint("puzzle", __name__)

@puzzle.route("/description", methods=["GET"])
def description():
    year = int(request.args.get("year"))
    day = int(request.args.get("day"))
    task = calendar[year][day](0)

    return jsonify({
        "description": task.description()
    })

@jwt_required()
@puzzle.route("/puzzle/all", methods=["GET"])
def puzzle_all():
    id = get_jwt_identity()
    competition = str(request.args.get("competition"))

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
@puzzle.route("/puzzle/details", methods=["GET"])
def puzzle_details():
    id = get_jwt_identity()
    competition = str(request.args.get("competition"))
    dayNum = str(request.args.get("competition"))

    try:
        days = calendar[competition]
    except:
        raise RequestError("This competition does not exist")


    try:
        day = days[dayNum - 1]
    except:
        raise RequestError("This day does not exist")

    return jsonify(
        day(id).details() #changed outut structure a bit
    )

@jwt_required()
@puzzle.route("/puzzle/input", methods=["GET"])
def puzzle_input():
    id = get_jwt_identity()
    competition = str(request.args.get("competition"))
    dayNum = str(request.args.get("competition"))
    part = str(request.args.get("part")) #assume this will be there

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
