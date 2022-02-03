from flask import Blueprint, jsonify, request

from advent.calendar.calendar import calendar

advent = Blueprint("advent", __name__)

@advent.route("/description", methods=["GET"])
def description():
    year = int(request.args.get("year"))
    day = int(request.args.get("day"))
    task = calendar[year][day](0)

    return jsonify({
        "description": task.description()
    })
