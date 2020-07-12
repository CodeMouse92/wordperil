from PySide2.QtWidgets import QGridLayout, QWidget

from .puzzleboard import PuzzleBoard


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Word Peril")

        # Create layout and add widgets
        layout = QGridLayout()

        # Create widgets
        board = PuzzleBoard()
        layout.addWidget(board, 0, 0)

        # Set dialog layout
        self.setLayout(layout)
