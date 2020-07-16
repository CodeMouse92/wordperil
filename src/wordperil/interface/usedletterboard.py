from enum import Enum

from PySide2.QtWidgets import QGridLayout, QLabel, QFrame, QWidget
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class LetterStatus(Enum):
    HIDDEN = 0
    SHOWN = 1


class UsedLetter(QLabel):
    """A single letter tile on the board."""

    style_hidden = """
        background-color: blue;
        color: blue;
    """
    style_shown = """
        background-color: blue;
        color: white;
    """
    font = QFont("mono", 22)

    def __init__(self, letter=None, parent=None, **kwargs):
        super().__init__(letter, parent=parent, **kwargs)

        # Widget styling
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(2)

        # Text styling
        self.setFont(self.font)
        self.setAlignment(Qt.AlignCenter)
        self.setMargin(5)

        if letter:
            self.text = letter
        else:
            self.text = "#"

        # By default, each letter is hidden.
        self.setHidden()

    def setHidden(self):
        self.status = LetterStatus.HIDDEN
        self.setStyleSheet(self.style_hidden)

    def setShown(self):
        if self.text != "#":
            self.status = LetterStatus.SHOWN
            self.setStyleSheet(self.style_shown)

    def isShown(self):
        return self.status == LetterStatus.SHOWN


class UsedLetterBoard(QWidget):
    """The category/clue for the puzzle."""

    PER_ROW = 5

    stylesheet = """
        background-color: blue;
        color: white;
    """
    font = QFont("mono", 18)

    letter_positions = {
        "A": (0, 0),
        "E": (0, 1),
        "I": (0, 2),
        "O": (0, 3),
        "U": (0, 4),
        "B": (1, 0),
        "C": (1, 1),
        "D": (1, 2),
        "F": (1, 3),
        "G": (1, 4),
        "H": (2, 0),
        "J": (2, 1),
        "K": (2, 2),
        "L": (2, 3),
        "M": (2, 4),
        "N": (3, 0),
        "P": (3, 1),
        "Q": (3, 2),
        "R": (3, 3),
        "S": (3, 4),
        "T": (4, 0),
        "V": (4, 1),
        "W": (4, 2),
        "X": (4, 3),
        "Y": (4, 4),
        "Z": (5, 2),
    }

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Create layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        self.letters = {}

        for letter, (i, j) in self.letter_positions.items():
            self.letters[letter] = UsedLetter(letter)
            layout.addWidget(self.letters[letter], i, j)

        self.setLayout(layout)

    def reset(self):
        for letter in self.letters.values():
            letter.setHidden()

    def showLetter(self, letter):
        self.letters[letter.upper()].setShown()

    def hideLetter(self, letter):
        self.letters[letter.upper()].setHidden()

    def usedLetter(self, letter):
        return self.letters[letter.upper()].isShown()
