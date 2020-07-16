import json
from pathlib import Path
from appdirs import user_data_dir


class UsedCache:
    primary = None

    @classmethod
    def getPrimary(cls):
        if cls.primary is None:
            cls.primary = cls()
        return cls.primary

    def __init__(self):
        self.cache = {}
        self.directory = Path(user_data_dir('wordperil', 'codemouse92'))
        self.directory.mkdir(parents=True, exist_ok=True)
        self.filename = 'used.json'
        self.path = self.directory / self.filename
        self.path_tmp = self.directory / (self.filename + '.tmp')

        try:
            with self.path.open('r') as file:
                cache = json.load(file)
                for puzzleset, puzzles in cache.items():
                    self.cache[puzzleset] = set()
                    for puzzle in puzzles:
                        self.cache[puzzleset].add(tuple(puzzle))
        except FileNotFoundError:
            self.cache = {}

    def flush(self, puzzleset):
        if puzzleset:
            self.cache.pop(puzzleset, None)
        self.write()

    def write(self):
        out = {}
        for puzzleset, puzzles in self.cache.items():
            out[puzzleset] = list(puzzles)
        with self.path_tmp.open('w') as file:
            json.dump(out, file)
        self.path_tmp.rename(self.path)

    def add(self, puzzleset, puzzle_raw):
        if puzzleset not in self.cache:
            self.cache[puzzleset] = set()
        self.cache[puzzleset].add(puzzle_raw)
        self.write()

    def get(self, puzzleset):
        cache = set()
        if puzzleset.upper() in self.cache:
            for pair in self.cache[puzzleset]:
                cache.add(tuple(pair))
        return cache
