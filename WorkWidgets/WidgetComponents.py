from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=500))
        self.setText(content)


class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", placeholder_text="", length=10, width=300, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.setPlaceholderText(placeholder_text)


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Arial", font_size))

class ListWidgetComponent(QtWidgets.QListWidget):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", font_size))

class TextEditComponent(QtWidgets.QTextEdit):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", font_size))

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, items=None):
        super().__init__()
        if items:
            self.addItems(items)
        self.setFont(QtGui.QFont("Arial", 16))

    def update_items(self, items):
        self.clear()
        self.addItems(items)
