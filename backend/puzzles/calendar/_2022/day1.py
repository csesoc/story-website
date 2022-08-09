from common.exceptions import RequestError
from common.database import createSolve, findPid, getNumSolved, checkSolve
from puzzles.day import Day
from random import random
import json
from datetime import datetime

# TODO: sample Day 1 which has 1 part
class Day1(Day):
    def __init__(self, id):
        super().__init__(id)
        self.name = "Puzzle for day 1"
        self.part1Status = self.setpart1Status()
        self.part1Answer = self.setPart1Answer()
        self.parts = [{
                    "partNum": 1,
                    "description": "Add two numbers",
                    "solved": self.part1Status,
                    "answer": self.part1Answer
        }]

    def description(self):
        return {
            "n_parts": 1,
            "name": self.name,
            "dayNum": 1,
            "parts": self.parts
        }

    def generate_input(self, part):
        try:
            f = open("day1part" + str(part) + "_inputs.json")
        except:
            raise RequestError("This part does not exist")

        data = json.load(f)[self.hash()]
        f.close()
        return data


    def verify(self, solution, part):
        try:
            f = open("day1part" + str(part) + "_answers.json")
        except:
            raise RequestError("This part does not exist")

        ver = json.load(f)[self.hash()] == str(solution)

        if ver == True:
            pid = findPid("2022 Advent of Code", 1, part)
            time_stamp = datetime.now()
            numSolved = getNumSolved("2022 Advent of Code", 1, part, self.id)
            createSolve(self.id, pid, time_stamp, 1000 - getNumSolved)

        f.close()
        return {
            "correct": ver,
            "reason": ""
        }

    def hash(self):
        # mod based on size of inputs pool + 1
        return self.id % 5

    def setpart1Status(self):
        return checkSolve("2022 Advent of Code", 1, 1, self.id)

    def setPart1Answer(self):
        answer = ""
        if self.part1Status == True:
            f = open("day1part1_answers")
            answer = json.load(f)[self.hash()]
            f.close()

        return answer
