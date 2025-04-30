# filepath: minimal_test.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Minimal Test")
label = QLabel("Hello PyQt6!", parent=window)
window.setGeometry(100, 100, 200, 50)
window.show()
sys.exit(app.exec())