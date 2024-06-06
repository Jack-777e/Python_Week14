from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=500))
        self.setText(content)


class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        # self.setText(default_content)
        self.setPlaceholderText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet(""" 
                            QLineEdit:disabled{
                                background-color: AliceBlue;
                            }
                            QLineEdit:focus{
                                background-color: #C0FFFF;
                            }
                           """)


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet(""" 
                            QPushButton:disabled{
                                background-color: LightSlateGray;
                            }
                           """)


class ListWidgetComponent(QtWidgets.QListWidget):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", font_size))


class TextEditComponent(QtWidgets.QTextEdit):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", font_size))


class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, font_size=16):
        super().__init__()
        self.setEditable(True)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.lineEdit().setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet("""
                            QComboBox:disabled{
                                background-color: AliceBlue;
                            }
                            QComboBox:focus{
                                background-color: #B0FFFF;
                            }
                           """)