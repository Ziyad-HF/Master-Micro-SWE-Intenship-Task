from PySide2.QtWidgets import QApplication
from widgets.main_window import MainWindow
from utils import load_stylesheet
import sys


def main():
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    stylesheet = load_stylesheet("../resources/style.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
