import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow # Import the main window class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())