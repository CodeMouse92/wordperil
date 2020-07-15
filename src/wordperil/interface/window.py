from PySide2.QtWidgets import QGridLayout, QWidget, QPushButton
from PySide2.QtCore import Qt

from .controller import Controller, ControllerMode
from .puzzleboard import PuzzleBoard
from .usedletterboard import UsedLetterBoard
from .scoreboard import ScoreBoard
from .statusbar import StatusBar

from wordperil.model.puzzle import Puzzle


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

        self.controller = Controller(self)
        self.layout.addWidget(self.controller, 0, 0, 1, -1)

        self.usedletters = UsedLetterBoard()
        self.layout.addWidget(self.usedletters, 1, 0, 4, 1)

        self.board = PuzzleBoard()
        self.layout.addWidget(self.board, 1, 1, 4, 3)

        self.scores = ScoreBoard()
        self.layout.addWidget(self.scores, 5, 0, 2, -1)

        self.statusbar = StatusBar()
        self.layout.addWidget(self.statusbar, 7, 0, 1, -1)

    # MAJOR MODE FUNCTIONS

    """
    SETUP MODE

    Puzzle board: Shows current puzzle file name.
    Score Board: Blank. Disabled name fields.
    Solve Bar: Disabled, shows instructions.

    [L] - brings up dialog for loading puzzle file.
    [P] - toggle player count.
    [ENTER] - start round.
    """
    def setupMode(self):
        self.showMessage("word peril", "No puzzle set loaded.")
        self.lockNames()
        self.showStatus("[L] to load puzzle set | [ENTER] to start.")
        self.controller.setMode(ControllerMode.SETUP)

    """
    PLAYER MODE

    Puzzle board shows messages.
    Enabled name fields.
    Disabled status bar.
    """
    def playersMode(self):
        self.showMessage("Who's playing?", "[TAB] and enter names.")
        self.unlockNames()
        self.showStatus("3 players | [ENTER] to start | [ESC] to cancel.")
        self.controller.setMode(ControllerMode.PLAYERS)

    """
    SCORE MODE

    Puzzle board: Shows rounds completed/remaining and leader.
    Scores: Current scores, highest highlighted. Disabled name fields.
    Solve field: Disabled, shows instructions.

    [N] - next round
    [E] - end round
    """
    def scoreMode(self):
        self.showMessage("word peril", "No puzzle set loaded.")
        self.lockNames()
        self.showStatus("[N] for next round | [ESC] to end game")
        self.controller.setMode(ControllerMode.SCORE)

    """
    PUZZLE MODE

    Disabled name fields.
    Enabled status bar.

    [LETTER] guesses letter.
    [TAB]/click to solve puzzle.
    """
    def puzzleMode(self):
        self.loadPuzzle()
        self.lockNames()
        self.scores.nextPlayer()
        self.showPrompt("[TAB] and enter solution to solve.")
        self.controller.setMode(ControllerMode.PUZZLE)

    # UTILITY FUNCTIONS

    def showMessage(self, message, prompt):
        """Unload puzzle and show message on board instead."""
        self.usedletters.reset()
        self.board.showMessage(message, prompt)

    def showStatus(self, status):
        """Show message in status bar."""
        self.statusbar.showMessage(status)

    def showPrompt(self, prompt):
        """Show prompt in status bar, and allow user to input."""
        self.statusbar.showPrompt(prompt)

    def loadPuzzle(self):
        """Load a puzzle into the gameboard."""
        self.usedletters.reset()
        # TODO: Load a puzzle from the model
        puzzle = Puzzle("guido's time machine", clue="Phrase")
        self.board.loadPuzzle(puzzle)

    def lockNames(self):
        self.scores.lockNames()

    def unlockNames(self):
        self.scores.unlockNames()

    def guess(self, letter):
        """Guess a letter, updating the score of the current player."""
        if letter.isalpha():
            self.usedletters.showLetter(letter)
            correct = self.board.reveal(letter)
            # HACK
            print(correct)
        else:
            raise TypeError("Cannot guess non-letter.")
