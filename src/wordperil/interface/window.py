from PySide2.QtWidgets import QGridLayout, QWidget

from .puzzleboard import PuzzleBoard
from .usedletterboard import UsedLetterBoard
from .scoreboard import ScoreBoard


class Window(QWidget):

    _primary_window = None

    @classmethod
    def primary(cls, *args, **kwargs):
        if not cls._primary_window:
            cls._primary_window = Window(*args, **kwargs)
        return cls._primary_window

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Word Peril")
        self.setStyleSheet("background-color: black;")

        # Create layout and add widgets
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.usedletters = UsedLetterBoard()
        self.layout.addWidget(self.usedletters, 0, 0, 3, 1)

        self.board = PuzzleBoard()
        self.layout.addWidget(self.board, 0, 1, 3, 3)

        self.scores = ScoreBoard()
        self.layout.addWidget(self.scores, 3, 0, 1, -1)

    def showMessage(self, message, prompt):
        self.board.showMessage(message, prompt)

    def loadPuzzle(self, puzzle):
        """Load a puzzle into the gameboard."""
        self.usedletters.reset()
        self.board.loadPuzzle(puzzle)

    def guess(self, letter):
        """Guess a letter, updating the score of the current player."""
        if letter.isalpha():
            self.usedletters.showLetter(letter)
            correct = self.board.reveal(letter)
            # HACK
            print(correct)
        else:
            raise TypeError("Cannot guess non-letter.")
