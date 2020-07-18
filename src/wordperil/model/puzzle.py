from wordperil.common.constants import TILES_HORIZONTAL, TILES_VERTICAL


class Puzzle:
    @staticmethod
    def extract_row(string):
        length = 0
        line = ""
        unused = ""
        for word in string.split():
            length += len(word) + 1
            if length > TILES_HORIZONTAL:
                unused = f"{unused} {word}"
            else:
                line = f"{line} {word}"

        line = line.strip().center(TILES_HORIZONTAL)
        return (line, unused)

    @classmethod
    def validate(cls, puzzle):
        lines = 0
        puzzle = puzzle.upper()
        while puzzle and lines <= TILES_VERTICAL + 1:
            line, puzzle = cls.extract_row(puzzle)
            lines += 1
        return (lines < TILES_VERTICAL + 1)

    def __init__(self, puzzle, clue=""):
        self.clue = clue

        puzzle = puzzle.upper()
        self.puzzle_text = puzzle

        # Break the puzzle down into rows to fit on puzzle board
        self.rows = []
        while puzzle:
            line, puzzle = self.extract_row(puzzle)
            self.rows.append(line)
            if len(self.rows) > TILES_VERTICAL:
                raise ValueError("Cannot fit puzzle.")

        empty_rows = TILES_VERTICAL - len(self.rows)
        if empty_rows < 0:
            raise ValueError("Cannot fit puzzle.")
        elif empty_rows >= TILES_VERTICAL // 2:
            for row in range(empty_rows // 2):
                self.rows.insert(0, "".center(TILES_HORIZONTAL))

    def __hash__(self):
        return hash(self.puzzle_text)

    def __iter__(self):
        return iter(self.rows)

    def __str__(self):
        return self.puzzle_text
