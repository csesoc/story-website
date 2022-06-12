from flask import Blueprint, jsonify, request

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
