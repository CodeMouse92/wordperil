from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QLCDNumber
)
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class ScoreWidget(QWidget):
    normal_style = """
        background-color: black;
        color: green;
    """
    highlight_style = """
        background-color: green;
        color: white;
    """

    font = QFont("mono", 22)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.score = QLCDNumber()
        self.score.setMinimumHeight(80)
        self.score.setStyleSheet(self.normal_style)
        self.layout.addWidget(self.score)

        self.player = QLineEdit()
        self.player.setStyleSheet(self.normal_style)
        self.player.setFont(self.font)
        self.player.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.player)

    def lock(self):
        self.player.setReadOnly(True)
        self.player.setFocusPolicy(Qt.NoFocus)

    def unlock(self):
        self.score.display(0)
        self.player.setReadOnly(False)
        self.player.setFocusPolicy(Qt.StrongFocus)

    def highlight(self):
        self.player.setStyleSheet(self.highlight_style)
        self.score.setStyleSheet(self.highlight_style)

    def unhighlight(self):
        self.player.setStyleSheet(self.normal_style)
        self.score.setStyleSheet(self.normal_style)

    def adjustScore(self, score_adjustment):
        score = self.score.intValue() + score_adjustment
        self.score.display(score)

    def getScore(self):
        return self.score.intValue()


class ScoreBoard(QWidget):
    PLAYERS = 3

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.players = self.PLAYERS
        self.focus_player = None

        self.lastScore = None

        self.scores = []

        for _ in range(self.players):
            score = ScoreWidget(parent=self)
            self.scores.append(score)
            self.layout.addWidget(score)

    def unlockNames(self):
        """Erase scores and unlock names for editing."""
        self.unhighlight()
        for score in self.scores:
            score.unlock()

    def lockNames(self):
        for score in self.scores:
            score.lock()

    def verifyNames(self):
        for player in self.scores:
            if player.player.text().strip() == "":
                return False
        return True

    def undoLast(self):
        if self.lastScore:
            self.unhighlight()
            self.focus_player = self.lastScore[0]
            self.scores[self.focus_player].highlight()
            self.adjustScore(-(self.lastScore[1]))
            self.lastScore = None

    def nextPlayer(self):
        if self.focus_player is None:
            self.focus_player = -1

        self.unhighlight()

        self.focus_player += 1
        if self.focus_player >= self.players:
            self.focus_player = 0

        self.scores[self.focus_player].highlight()

    def unhighlight(self):
        """Unhighlight all scores."""
        for score in self.scores:
            score.unhighlight()

    def showHighest(self):
        """Highlights the highest scoring player(s)."""
        highest = 0
        leader = []
        self.unhighlight()
        for player in self.scores:
            score = player.getScore()
            if score > highest:
                highest = score
                leader = [player]
            if score == highest:
                leader.append(player)
        if leader and highest > 0:
            for player in leader:
                player.highlight()

    def adjustScore(self, score):
        self.lastScore = (self.focus_player, score)
        self.scores[self.focus_player].adjustScore(score)

    def reset(self):
        self.lastScore = None
        for score in self.scores:
            score.reset()
