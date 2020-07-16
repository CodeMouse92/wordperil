import random
from .puzzle import Puzzle


class Puzzleset:

    loaded = None

    @classmethod
    def loadFromPath(cls, path):
        try:
            with path.open() as file:
                title = file.readline().strip()
                puzzles = file.readlines()
                cls.loaded = Puzzleset(title, *puzzles)
                return True
        except (FileNotFoundError, NotADirectoryError):
            return False

    @classmethod
    def getLoadedSet(cls):
        return cls.loaded

    @classmethod
    def isSetLoaded(cls):
        return (cls.loaded is not None)

    @classmethod
    def getLoadedSetTitle(cls):
        if cls.loaded is None:
            return "No puzzle set loaded."
        else:
            return f"{cls.loaded.title} ({len(cls.loaded.puzzles)} puzzles)"

    def __init__(self, title, *puzzles):
        self.title = title
        self.puzzles = set()
        self.used = set()  # TODO: Load from saved files
        for puzzle in puzzles:
            if puzzle.strip() == "":
                continue
            clue, text = puzzle.split(sep='|', maxsplit=1)
            self.puzzles.add(Puzzle(text.strip(), clue.strip()))
        # Remove all used puzzles from set
        self.puzzles.difference_update(self.used)

    def getPuzzle(self):
        return random.sample(self.puzzles, 1)[0]