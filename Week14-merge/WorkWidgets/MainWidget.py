from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.AddModifyStuWidget import AddModifyStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.WidgetComponents import *
from SocketClient import SocketClient


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")
        self.setStyleSheet("""
            QWidget#main_widget {
                background-color: #e3f2fd;
            }
            QLabel {
                color: #0d47a1;
            }
        """)
        
        self.socket = SocketClient()

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")
        function_widget = FunctionWidget(self.socket)
        menu_widget = MenuWidget(function_widget.update_widget)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(menu_widget, 1, 0, 1, 1)
        layout.addWidget(function_widget, 1, 1, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)

        self.setLayout(layout)

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback
        self.setStyleSheet("""
            QWidget#menu_widget {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QtWidgets.QVBoxLayout()
        add_modify_button = ButtonComponent("Add / Modify")
        del_button = ButtonComponent("Del student")
        show_button = ButtonComponent("Show all")
        add_modify_button.clicked.connect(lambda: self.update_widget_callback("add / modify"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))

        layout.addWidget(add_modify_button, stretch=1)
        layout.addWidget(del_button, stretch=1)
        layout.addWidget(show_button, stretch=1)

        self.setLayout(layout)

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket
        self.widget_dict = {
            "add / modify": self.addWidget(AddModifyStuWidget(self.socket)),
            "del": self.addWidget(DelStuWidget(self.socket)),
            "show": self.addWidget(ShowStuWidget(self.socket))
        }
        self.update_widget("add / modify")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()