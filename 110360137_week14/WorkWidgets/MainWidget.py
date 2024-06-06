from PyQt6 import QtWidgets,QtCore,QtGui
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")
        self.setStyleSheet("background-color: black;") 
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.changeColor)
        self.timer.start(50)  
        self.color = QtGui.QColor(255, 0, 0)  
        layout = QtWidgets.QVBoxLayout()
        
        # Header label
        self.header_label = LabelComponent(28, "學生成績管理系統")
        self.header_label.setStyleSheet("color: yellow;")  
        
        # Function and menu widgets
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)
        
        # Add widgets to layout
        layout.addWidget(self.header_label)
        layout.addWidget(menu_widget)
        layout.addWidget(function_widget)
        
        # Set layout stretch factors
        layout.setStretchFactor(self.header_label, 1)
        layout.setStretchFactor(menu_widget, 1)
        layout.setStretchFactor(function_widget, 6)
        
        self.setLayout(layout)
    
    def changeColor(self):
        self.color = self.color.toHsv()  # Convert color to HSV
        h = (self.color.hue() + 1) % 360  # Increment hue
        self.color.setHsv(h, 255, 255)  # Set new hue value
        self.header_label.setStyleSheet("color: " + self.color.name())


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback
        
        layout = QtWidgets.QHBoxLayout()
        
        add_button = ButtonComponent("新增學生")
        del_button = ButtonComponent("刪除學生")
        modify_button = ButtonComponent("更改成績")
        show_button = ButtonComponent("成績列表")
        
        button_style = """
            QPushButton {
                color: white;
                border: 2px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: gray;
            }
        """
        
        add_button.setStyleSheet(button_style)
        del_button.setStyleSheet(button_style)
        modify_button.setStyleSheet(button_style)
        show_button.setStyleSheet(button_style)
        
        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))
        
        layout.addWidget(add_button)
        layout.addWidget(del_button)
        layout.addWidget(modify_button)
        layout.addWidget(show_button)
        
        self.setLayout(layout)


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "add": AddStuWidget(),
            "del": DelStuWidget(),
            "modify": ModifyStuWidget(),
            "show": ShowStuWidget()
        }
        
        for key, widget in self.widget_dict.items():
            widget.setStyleSheet("color: white;")  
            self.addWidget(widget)
        
        self.update_widget("add")
    
    def update_widget(self, name):
        if name in self.widget_dict:
            self.setCurrentWidget(self.widget_dict[name])
            current_widget = self.currentWidget()
            if current_widget is not None:
                current_widget.load()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_widget = MainWidget()
    main_widget.show()
    app.exec()
