from PySide2.QtWidgets import QGridLayout, QWidget

from wordperil.model.puzzle import Puzzle

from .puzzleboard import PuzzleBoard
from .usedletterboard import UsedLetterBoard


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Word Peril")
        self.setStyleSheet("background-color: black;")

        # Create layout and add widgets
        layout = QGridLayout()

        self.usedletters = UsedLetterBoard()
        layout.addWidget(self.usedletters, 0, 0, 2, 1)

        # Create widgets
        self.board = PuzzleBoard()
        layout.addWidget(self.board, 0, 1, 2, 3)

        # HACK: temporary
        self.board.setPuzzle(Puzzle("ask forgiveness not permission", clue="Phrase"))
        self.usedletters.showLetter("A")
        self.usedletters.showLetter("D")
        self.usedletters.showLetter("Z")
        self.usedletters.showLetter("M")

        # Set dialog layout
        self.setLayout(layout)
