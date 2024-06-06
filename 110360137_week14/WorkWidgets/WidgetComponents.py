from PyQt6 import QtWidgets, QtCore, QtGui

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()
        self.setWordWrap(True)
        self.setStyleSheet("font-weight: bold;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setFont(QtGui.QFont("微軟正黑體", pointSize=font_size, weight=500))
        self.setText(content)

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", placeholder_text="", length=10, width=300, font_size=20):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setPlaceholderText(placeholder_text)

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, items=None, font_size=20):
        super().__init__()
        self.setEditable(True)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        if items:
            self.addItems(items)
        self.setMinimumHeight(30)
        self.setMaximumWidth(300)
        
