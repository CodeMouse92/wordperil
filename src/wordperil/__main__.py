import sys
from PySide2.QtWidgets import QApplication

from wordperil.interface import Window


def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = Window.primary()
    window.show()

    window.setupMode()

    # Run the main Qt loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
