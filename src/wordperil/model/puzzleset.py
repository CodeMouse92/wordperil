import random

import json
from .puzzle import Puzzle
from .usedcache import UsedCache


class Puzzleset:

    loaded = None

    @classmethod
    def loadFromPath(cls, path):
        try:
            cls.loaded = Puzzleset(path)
        except (FileNotFoundError, NotADirectoryError):
            print(f"{path} is not a valid path.")
        except (IsADirectoryError, json.decoder.JSONDecodeError):
            print(f"{path} is not a valid puzzle set file.")

    @classmethod
    def getLoadedSet(cls):
        return cls.loaded

    @classmethod
    def isSetLoaded(cls):
        return (cls.loaded is not None)

    @classmethod
    def getLoadedSetTitle(cls, count=True, default="No puzzle set loaded."):
        if cls.loaded is None:
            return default
        elif count:
            return f"{cls.loaded.title} ({len(cls.loaded)} puzzles)"
        else:
            return cls.loaded.title

    def __init__(self, path):
        with path.open() as file:
            data = json.load(file)
            title = tuple(data.keys())[0]
            self.title = title.upper()
            self.puzzles = set()
            for clue, puzzles in data[title].items():
                for puzzle in puzzles:
                    self.puzzles.add(
                        (
                            puzzle.strip().upper(),
                            clue.strip().upper()
                        )
                    )
            # TODO: Prevalidate puzzles

    def __len__(self):
        used = UsedCache.getPrimary().get(self.title)
        return len(self.puzzles.difference(used))

    def markUsed(self, puzzle_raw):
        UsedCache.getPrimary().add(self.title, puzzle_raw)
        UsedCache.getPrimary().write()

    def getPuzzle(self):
        used = UsedCache.getPrimary().get(self.title)
        avail = self.puzzles.difference(used)
        selection = random.sample(avail, 1)[0]
        puzzle_text, clue = selection
        try:
            puzzle = Puzzle(puzzle_text, clue=clue)
            self.markUsed(selection)
            return puzzle
        except ValueError:
            return self.getPuzzle()
