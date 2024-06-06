from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import *
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.WidgetComponents import *

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")
        self.setWindowTitle('Student Management System')
        window_icon = QIcon("Picture/classroom.png")
        self.setWindowIcon(window_icon)
        self.setStyleSheet("""
            QWidget#main_widget {
                background-color: #f0dcdd;
            }
            QLabel {
                color: #79606a;
            }
        """)

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")
        
        function_widget = FunctionWidget()
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
            QPushButton {
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
        """)

        layout = QtWidgets.QVBoxLayout()
        add_button = ButtonComponent("Add student")
        del_button = ButtonComponent("Delete student")
        modify_button = ButtonComponent("Modify student")
        show_button = ButtonComponent("Show all")

        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))

        layout.addWidget(add_button, stretch=1)
        layout.addWidget(del_button, stretch=1)
        layout.addWidget(modify_button, stretch=1)
        layout.addWidget(show_button, stretch=1)

        self.setLayout(layout)


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "add": self.addWidget(AddStuWidget()),
            "del": self.addWidget(DelStuWidget()),
            "modify": self.addWidget(ModifyStuWidget()),
            "show": self.addWidget(ShowStuWidget())
        }
        self.update_widget("add")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()