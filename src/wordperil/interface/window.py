from pathlib import Path

from PySide2.QtWidgets import QGridLayout, QWidget, QFileDialog
from PySide2.QtCore import Qt

from .controller import Controller, ControllerMode
from .puzzleboard import PuzzleBoard
from .scoreboard import ScoreBoard
from .solvebar import SolveBar

from wordperil.common import constants
from wordperil.model.puzzleset import Puzzleset
from wordperil.model.usedcache import UsedCache


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

        self.controller = Controller(parent=self)
        self.layout.addWidget(self.controller, 0, 0, 1, -1)

        self.board = PuzzleBoard(parent=self)
        self.layout.addWidget(self.board, 1, 0, 4, -1)

        self.scores = ScoreBoard(parent=self)
        self.layout.addWidget(self.scores, 5, 0, 2, -1)

        self.solvebar = SolveBar(parent=self)
        self.layout.addWidget(self.solvebar, 7, 0, 1, -1)

    # MAJOR MODE FUNCTIONS

    """
    SETUP MODE

    Puzzle board: Shows current puzzle file name.import
    """
    def setupMode(self):
        self.showMessage("word peril", Puzzleset.getLoadedSetTitle())
        self.unlockNames()  # this also resets the scoreboard
        self.lockNames()
        self.showStatus("[L] to load puzzle set | [ENTER] to start.")
        self.controller.setMode(ControllerMode.SETUP)

    """
    PLAYER MODE

    Puzzle board shows messages.
    Enabled name fields.
    Disabled solve bar.
    """
    def playersMode(self):
        if Puzzleset.isSetLoaded() and not Puzzleset.isSetExhausted():
            self.showMessage("Who's playing?", "[TAB] to enter names.")
            self.showAction("")
            self.unlockNames()
            self.showStatus(
                "[TAB] past names and [ENTER] to start | [ESC] to cancel."
            )
            self.controller.setMode(ControllerMode.PLAYERS)
        elif Puzzleset.isSetExhausted():
            self.showAction("Set Exhausted!")
            self.setupMode()

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
    Enabled solve bar.

    [LETTER] guesses letter.
    [TAB]/click to solve puzzle.
    """
    def puzzleMode(self):
        if Puzzleset.isSetExhausted():
            self.showAction("Set Exhausted!")
        else:
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
        if not filename[0]:
            return
        try:
            Puzzleset.loadFromPath(Path(filename[0]))
        except FileNotFoundError:
            self.showAction("File not found")
        except ValueError:
            self.showAction("Invalid file")
        else:
            self.showMessage("word peril", Puzzleset.getLoadedSetTitle())
            self.showAction("Set Loaded!")

    def clearCache(self):
        puzzleset = Puzzleset.getLoadedSetTitle(count=False, default="")
        if puzzleset:
            UsedCache.getPrimary().flush(puzzleset)
            self.showMessage("word peril", Puzzleset.getLoadedSetTitle())
            self.showAction("Reset puzzle set!")

    def showMessage(self, message, prompt):
        """Unload puzzle and show message on board instead."""
        self.board.showMessage(message, prompt)

    def showAction(self, action):
        """Announce an action in the counter."""
        self.board.showAction(action)

    def showStatus(self, status):
        """Show message in solve bar."""
        self.solvebar.showMessage(status)

    def showPrompt(self, prompt):
        """Show prompt in solve bar, and allow user to input."""
        self.solvebar.showPrompt(prompt)

    def loadPuzzle(self):
        """Load a puzzle into the gameboard."""
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

        letter = letter.upper()
        correct = self.board.guess(letter)
        if correct > 0:
            # Gain points for correct letters.
            if letter in 'AEIOU':
                score_change = constants.SCORE_CORRECT_VOWEL * correct
                self.scores.adjustScore(score_change)
            else:
                score_change = constants.SCORE_CORRECT_CONSONANT * correct
                self.scores.adjustScore(score_change)
        elif correct < 0:
            # Lose points for incorrect letters.
            score_change = constants.SCORE_INCORRECT_LETTER
            self.scores.adjustScore(score_change)
            # Move on to next player.
            self.scores.nextPlayer()
        elif correct == 0:
            # Already used, move on to next player.
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

    def undoLast(self):
        self.scores.undoLast()
        self.board.undoLast()
