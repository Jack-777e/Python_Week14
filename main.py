from WorkWidgets.MainWidget import MainWidget
from PyQt6.QtWidgets import QApplication
from PyQt6 import sip
import sys


app = QApplication([])
main_window = MainWidget()

main_window.setFixedSize(800, 600)
main_window.show()

sys.exit(app.exec())


