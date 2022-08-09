from common.exceptions import RequestError
from puzzles.day import Day
from random import random

# TODO: sample Day 1 which has 1 part
class Day1(Day):
    def __init__(self, id):
        super().__init__(id)
        self.name = "Puzzle for day 1"
        self.part1Status = False
        self.part1Answer = ""
        self.parts = {
                    "partNum": 1,
                    "description": "Add two numbers",
                    "solved": self.part1Status,
                    "answer": self.part1Answer
        }
        self.inputs = [
            str(random()) + " " + str(random())
        ]

    def description(self):
        return {
            "n_parts": 1,
            "name": self.name,
            "dayNum": 1,
            "parts": self.parts
        }

    def generate_input(self, part):
        try:
            return self.inputs[part - 1]
        except:
            raise RequestError("This part does not exist")


    def verify(self, solution, part):
        return self.id == int(solution)
