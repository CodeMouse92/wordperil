from PySide2.QtWidgets import QLineEdit
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class StatusBar(QLineEdit):

    style = """
        background-color: black;
        color: green;
    """

    font = QFont("mono", 18)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(self.font)
        self.setStyleSheet(self.style)
        self.lock()

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
