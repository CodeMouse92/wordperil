from enum import Enum

from PySide2.QtWidgets import QGridLayout, QVBoxLayout, QLabel, QFrame, QWidget
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class TileStatus(Enum):
    UNUSED = 0
    HIDDEN = 1
    GLOW = 2
    SHOWN = 3


class Tile(QLabel):
    """A single letter tile on the board."""

    style_unused = """
        background-color: blue;
        color: blue;
    """
    style_hidden = """
        background-color: green;
        color: green;
    """
    style_glow = """
        background-color: white;
        color: white;
    """
    style_shown = """
        background-color: green;
        color: white;
    """
    font = QFont("mono", 24)

    def __init__(self, letter=None, **kwargs):
        super().__init__(letter, **kwargs)

        # Widget styling
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(3)

        # Text styling
        self.setFont(self.font)
        self.setAlignment(Qt.AlignCenter)
        self.setMargin(5)

        # Set letter and appropriate style
        self.setLetter(letter)

    def setLetter(self, letter=None):
        if letter is None or letter is " ":
            self.setText("#")
            self.status = TileStatus.UNUSED
            self.setStyleSheet(self.style_unused)
        else:
            if letter.isalpha():
                self.setText(letter)
                self.status = TileStatus.HIDDEN
                self.setStyleSheet(self.style_hidden)
            else:
                self.setText(letter)
                self.status = TileStatus.SHOWN
                self.setStyleSheet(self.style_shown)

    def reveal(self):
        self.status = TileStatus.SHOWN
        self.setStyleSheet(self.style_shown)


class Clue(QLabel):
    """The category/clue for the puzzle."""

    stylesheet = """
        background-color: blue;
        color: white;
    """
    font = QFont("mono", 20)

    def __init__(self, text="", **kwargs):
        super().__init__(text, **kwargs)

        # Widget styling
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)

        # Formatting
        self.setStyleSheet(self.stylesheet)
        self.setFont(self.font)
        self.setAlignment(Qt.AlignCenter)


class PuzzleGrid(QWidget):
    TILES_HORIZONTAL = 14
    TILES_VERTICAL = 4

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        # Generate board
        self.tiles = [
            [Tile() for _ in range(self.TILES_HORIZONTAL)]
            for _ in range(self.TILES_VERTICAL)
        ]
        for v, row in enumerate(self.tiles):
            for h, tile in enumerate(row):
                layout.addWidget(tile, v, h, 1, 1)

        self.setLayout(layout)

    def setPuzzle(self, puzzle):

        def extractRow(self, puzzle, row):
            length = 0
            line = ""
            unused = ""
            for word in puzzle.split():
                length += len(word) + 1
                if length > self.TILES_HORIZONTAL:
                    unused = f"{unused} {word}"
                else:
                    line = f"{line} {word}"

            line = line.center(self.TILES_HORIZONTAL - 1)
            for i, letter in enumerate(line):
                self.tiles[row][i].setLetter(letter)

            return unused

        # Determine how many rows are needed
        rows = len(puzzle) // self.TILES_HORIZONTAL

        # Capitalize puzzle
        puzzle = puzzle.upper()

        if rows <= (self.TILES_VERTICAL // 2):
            start_row = 1
            end_row = start_row + rows
        elif rows <= self.TILES_VERTICAL:
            start_row = 0
            end_row = start_row + rows
        else:
            raise ValueError("Cannot fit puzzle!")

        print(f"{rows} and {(self.TILES_VERTICAL // 2)}")

        for row in range(start_row, end_row + 1):
            puzzle = extractRow(self, puzzle, row)


class PuzzleBoard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout and add widgets
        self.layout = QVBoxLayout()

        self.puzzle = PuzzleGrid()
        self.layout.addWidget(self.puzzle)

        self.clue = Clue()
        self.layout.addWidget(self.clue)

        # Set dialog layout
        self.setLayout(self.layout)

        # HACK
        self.setPuzzle("Phrase", "ask forgiveness not permission")

    def setPuzzle(self, clue, puzzle):
        self.clue.setText(clue)
        self.puzzle.setPuzzle(puzzle)
