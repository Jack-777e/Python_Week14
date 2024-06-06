from PyQt6 import QtWidgets, QtCore, QtGui

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=500))
        self.setStyleSheet("""
            QLineEdit{
                background-color	: PowderBlue;
                border: 2px solid #00796b;
                border-radius: 7px;
                padding: 2px;}
            QLineEdit:focus{background-color: LightSkyBlue;}
            QLineEdit:disabled{background-color: #E8FFFF;}""")

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

class TextEditComponent(QtWidgets.QTextEdit):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet("""
            QTextEdit{
                border: 2px solid #00796b;
                border-radius: 8px;
                padding: 2px;}""")


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet("""
            QPushButton{
                background-color	: PowderBlue;
                border: none;
                border-radius: 12px;
                padding: 5px 10px;
                text-align: center;
                margin: 4px 2px;
                }
            QPushButton:hover{
                color : LightCyan;
                background-color	: #67AECB;
                }
            QPushButton:disabled{
                background-color	: #E8FFFF;
                }
            """)


class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, font_size=16):
        super().__init__()
        self.setEditable(True)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.lineEdit().setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet("""
            QComboBox{
                background-color	: PowderBlue;
                border: 2px solid #00796b;
                border-radius: 7px;
                padding: 2px;}
            QComboBox:focus{
                background-color	: LightSkyBlue;}
            QComboBox:disabled{
                background-color	: #E8FFFF;}
            """)
