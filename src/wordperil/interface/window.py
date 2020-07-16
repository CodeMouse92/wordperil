from pathlib import Path

from PySide2.QtWidgets import QGridLayout, QWidget, QFileDialog
from PySide2.QtCore import Qt

from .controller import Controller, ControllerMode
from .puzzleboard import PuzzleBoard
from .usedletterboard import UsedLetterBoard
from .scoreboard import ScoreBoard
from .statusbar import StatusBar

from wordperil.common import constants
from wordperil.model.puzzle import Puzzle
from wordperil.model.puzzleset import Puzzleset


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

        self.usedletters = UsedLetterBoard(self)
        self.layout.addWidget(self.usedletters, 1, 0, 4, 1)

        self.board = PuzzleBoard(self)
        self.layout.addWidget(self.board, 1, 1, 4, 3)

        self.scores = ScoreBoard(self)
        self.layout.addWidget(self.scores, 5, 0, 2, -1)

        self.statusbar = StatusBar(self)
        self.layout.addWidget(self.statusbar, 7, 0, 1, -1)

    # MAJOR MODE FUNCTIONS

    """
    SETUP MODE

    Puzzle board: Shows current puzzle file name.import
    """
    def setupMode(self):
        self.showMessage("word peril", Puzzleset.getLoadedSetTitle())
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
        if Puzzleset.isSetLoaded():
            self.showMessage("Who's playing?", "[TAB] to enter names.")
            self.unlockNames()
            self.showStatus("[TAB] past names and [ENTER] to start | [ESC] to cancel.")
            self.controller.setMode(ControllerMode.PLAYERS)

    """
    SCORE MODE

    Puzzle board: Shows rounds completed/remaining and leader.
    Scores: Current scores, highest highlighted. Disabled name fields.
    Solve field: Disabled, shows instructions.

    [N] - next round
    [E] - end round
    """
    def scoreMode(self, lastpuzzle="word peril"):
        if self.scores.verifyNames():
            self.controller.setFocus(Qt.OtherFocusReason)
            self.showMessage(lastpuzzle, Puzzleset.getLoadedSetTitle())
            self.lockNames()
            self.scores.showHighest()
            self.showStatus("[N] for next round | [ESC] to end game.")
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

    def loadPuzzleset(self):
        filename = QFileDialog.getOpenFileName(
            self,
            "Open Puzzle Set",
            str(Path.home()),
            "Word Peril Puzzle Sets (*.peril)"
        )
        if Puzzleset.loadFromPath(Path(filename[0])):
            self.showMessage("word peril", Puzzleset.getLoadedSetTitle())

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
        puzzleset = Puzzleset.getLoadedSet()
        if puzzleset:
            self.board.loadPuzzle(puzzleset.getPuzzle())

    def lockNames(self):
        self.scores.lockNames()

    def unlockNames(self):
        self.scores.unlockNames()

    def guess(self, letter):
        """Guess a letter, updating the score of the current player."""
        if not letter.isalpha():
            raise TypeError("Cannot guess non-letter.")

        if self.usedletters.usedLetter(letter):
            # If the letter is already guessed, moved on.
            self.scores.nextPlayer()
        else:
            letter = letter.upper()
            self.usedletters.showLetter(letter)
            correct = self.board.reveal(letter)
            if correct > 0:
                # Gain points for correct letters.
                if letter in 'AEIOU':
                    score_change = constants.SCORE_CORRECT_VOWEL * correct
                    self.scores.adjustScore(score_change)
                else:
                    score_change = constants.SCORE_CORRECT_CONSONANT * correct
                    self.scores.adjustScore(score_change)
            else:
                # Lose points for incorrect letters.
                score_change = constants.SCORE_INCORRECT_LETTER
                self.scores.adjustScore(score_change)
                # Move on to next player.
                self.scores.nextPlayer()

    def attemptSolve(self, solution):
        if self.board.attemptSolve(solution):
            score_change = constants.SCORE_CORRECT_SOLVE
            self.scores.adjustScore(score_change)
            self.scoreMode(self.board.puzzle_text)
        else:
            score_change = constants.SCORE_INCORRECT_SOLVE
            self.scores.adjustScore(score_change)
            self.scores.nextPlayer()
