from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QLCDNumber,
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
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.score = QLCDNumber()
        self.score.setMinimumHeight(80)
        self.score.setStyleSheet(self.normal_style)
        self.layout.addWidget(self.score)

        self.player = QLineEdit()
        self.player.setStyleSheet(self.normal_style)
        self.player.setFont(self.font)
        self.layout.addWidget(self.player)

    def lock(self):
        self.player.setReadOnly(True)
        self.player.setFocusPolicy(Qt.NoFocus)

    def unlock(self):
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


class ScoreBoard(QWidget):
    def __init__(self, players=3, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        if players < 1:
            raise ValueError("Must have at least one player.")
        elif players > 3:
            raise ValueError("Cannot have more than three players.")

        self.players = players
        self.focus_player = 0

        self.scores = []

        for _ in range(self.players):
            score = ScoreWidget()
            self.scores.append(score)
            self.layout.addWidget(score)

        # Start by highlighting the first player.
        self.scores[0].highlight()

    def unlockNames(self):
        for score in self.scores:
            score.unlock()

    def lockNames(self):
        for score in self.scores:
            score.lock()

    def nextPlayer(self):
        self.scores[self.focus_player].unhighlight()

        self.focus_player += 1
        if self.focus_player >= self.players:
            self.focus_player = 0

        self.scores[self.focus_player].highlight()

    def adjustScore(self, score):
        self.scores[self.focus_player].adjustScore(score)

    def reset(self):
        for score in self.scores:
            score.reset()
