from enum import Enum

from PySide2.QtWidgets import QGridLayout, QVBoxLayout, QLabel, QFrame, QWidget
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt

from wordperil.common.constants import TILES_HORIZONTAL, TILES_VERTICAL


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
        if letter is None or letter == " ":
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

    def __init__(self, **kwargs):
        super().__init__("", **kwargs)

        # Widget styling
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)

        # Formatting
        self.setStyleSheet(self.stylesheet)
        self.setFont(self.font)
        self.setAlignment(Qt.AlignCenter)

        self.setMaximumHeight(40)


class PuzzleGrid(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        # Generate board
        self.tiles = [
            [Tile() for _ in range(TILES_HORIZONTAL)]
            for _ in range(TILES_VERTICAL)
        ]
        for v, row in enumerate(self.tiles):
            for h, tile in enumerate(row):
                layout.addWidget(tile, v, h, 1, 1)

        self.setLayout(layout)

    def setPuzzle(self, puzzle):
        for i, row in enumerate(puzzle):
            for j, letter in enumerate(row):
                self.tiles[i][j].setLetter(letter)


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

    def setPuzzle(self, puzzle):
        self.clue.setText(puzzle.clue)
        self.puzzle.setPuzzle(puzzle)
