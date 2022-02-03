from advent.day import Day

# TODO: change to actual implementation
class Day1(Day):
    def __init__(self, id):
        super().__init__(id)

    def description(self):
        return "2022 Day 1"

    def generate_input(self):
        return self.id

    def verify(self, solution):
        return self.id == int(solution)
