from abc import ABC, abstractmethod

class Day(ABC):
    @abstractmethod
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def description(self) -> str:
        """
        The description for this day's puzzle.
        """

    @abstractmethod
    def generate_input(self) -> str:
        """
        Generates the input for this day's puzzle, which ideally is unique
        for each user ID. Must generate the same result every time for each
        user (i.e. be pure).
        """

    @abstractmethod
    def verify(self, solution) -> bool:
        """
        Checks that the user entered the correct solution for this day's puzzle.
        """
