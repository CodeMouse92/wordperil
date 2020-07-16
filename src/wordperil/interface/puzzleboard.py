import itertools
from enum import Enum

from PySide2.QtWidgets import QGridLayout, QVBoxLayout, QLabel, QFrame, QWidget
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt

from wordperil.common.constants import TILES_HORIZONTAL, TILES_VERTICAL
from wordperil.model.puzzle import Puzzle

from .usedletterboard import UsedLetterBoard


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
    font = QFont("mono", 32)

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
                self.hide()
            else:
                self.setText(letter)
                self.reveal()

    def reveal(self):
        if self.text() != "#":
            self.status = TileStatus.SHOWN
            self.setStyleSheet(self.style_shown)

    def hide(self):
        if self.text() != "#":
            self.status = TileStatus.HIDDEN
            self.setStyleSheet(self.style_hidden)


class Clue(QLabel):
    """The category/clue for the puzzle."""

    stylesheet = """
        background-color: blue;
        color: white;
    """
    font = QFont("mono", 22)

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
        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)

        self.tiles = []
        for v in range(TILES_VERTICAL):
            for h in range(TILES_HORIZONTAL):
                tile = Tile()
                self.tiles.append(tile)
                self.layout.addWidget(tile, v, h, 1, 1)

        self.setLayout(self.layout)

    def loadPuzzle(self, puzzle):
        i = 0
        for row in puzzle:
            for letter in row:
                self.tiles[i].setLetter(letter)
                i += 1

    def reveal(self, letter=None):
        revealed = 0
        for tile in self.tiles:
            if letter is None or tile.text() == letter.upper():
                tile.reveal()
                revealed += 1
        return revealed

    def hide(self, letter):
        for tile in self.tiles:
            if tile.text() == letter.upper():
                tile.hide()

    def clear(self):
        for tile in self.tiles:
            tile.setLetter(None)


class PuzzleBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout and add widgets
        self.layout = QGridLayout()

        self.usedletters = UsedLetterBoard(self)
        self.layout.addWidget(self.usedletters, 0, 0, 2, 1)

        self.puzzle = PuzzleGrid()
        self.layout.addWidget(self.puzzle, 0, 1, 1, 3)

        self.clue = Clue()
        self.layout.addWidget(self.clue, 1, 1, 1, 3)

        # Set dialog layout
        self.setLayout(self.layout)

        # Remember last actions
        self.lastGuess = None

    def loadPuzzle(self, puzzle):
        self.clue.setText(puzzle.clue)
        self.puzzle_text = puzzle.puzzle_text
        self.puzzle.clear()
        self.usedletters.reset()
        self.puzzle.loadPuzzle(puzzle)

    def showMessage(self, message, prompt):
        self.usedletters.reset()
        puzzle = Puzzle(message, clue=prompt)
        self.loadPuzzle(puzzle)
        self.puzzle.reveal()

    def guess(self, letter):
        # If the letter is already guessed, moved on.
        if self.usedletters.usedLetter(letter):
            # Mark that this guess has nothing to undo.
            self.lastGuess = None
            return 0
        self.lastGuess = letter
        self.usedletters.showLetter(letter)
        matches = self.reveal(letter)
        if matches > 0:
            return matches
        else:
            # If there were no matches, return -1.
            return -1

    def reveal(self, letter=None):
        if letter is None:
            self.puzzle.reveal()
        return self.puzzle.reveal(letter)

    def attemptSolve(self, guess):
        # Mark that this guess has nothing to undo.
        self.lastGuess = None

        guess = ''.join(filter(str.isalpha, guess.upper()))
        solution = ''.join(filter(str.isalpha, self.puzzle_text.upper()))
        if guess == solution:
            self.reveal()
            return True
        else:
            return False

    def undoLast(self):
        """Undo last guess."""
        if self.lastGuess:
            self.usedletters.hideLetter(self.lastGuess)
            self.puzzle.hide(self.lastGuess)
