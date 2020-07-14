import sys
from PySide2.QtWidgets import QApplication

from wordperil.interface import Window

from wordperil.model.puzzle import Puzzle


def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = Window.primary()
    window.show()

    window.showMessage("word peril", "Press L to load puzzles.")
    puzzle = Puzzle("guido's time machine", clue="Phrase")
    window.loadPuzzle(puzzle)
    window.guess('a')
    window.guess('s')
    window.guess('m')
    window.guess('v')
    window.guess('z')
    window.guess('r')
    puzzle = Puzzle("ask forgiveness not permission", clue="Phrase")
    window.loadPuzzle(puzzle)

    # Run the main Qt loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
