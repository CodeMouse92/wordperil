from PySide2.QtWidgets import QLineEdit
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class SolveBar(QLineEdit):

    style = """
        background-color: black;
        color: green;
    """

    font = QFont("mono", 18)

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.setAlignment(Qt.AlignCenter)
        self.setFont(self.font)
        self.setStyleSheet(self.style)
        self.lock()

        self.returnPressed.connect(self.onPressed)

    def onPressed(self):
        self.parent.attemptSolve(self.text())

    def showMessage(self, message):
        self.lock()
        self.setText(message)

    def showPrompt(self, message):
        self.setText("")
        self.unlock()
        self.setPlaceholderText(message)

    def getText(self):
        return self.text

    def unlock(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.setReadOnly(False)

    def lock(self):
        self.setFocusPolicy(Qt.NoFocus)
        self.setReadOnly(True)
