from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import *
from ExecuteCommand import ExecuteCommand
import json

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self, socket):
        super().__init__()
        self.setObjectName("del_stu_widget")
        self.socket = socket
        
        layout = QtWidgets.QGridLayout()
        
        self.setting_content_label()
        self.setting_editor_label()
        self.setting_button()
        
        layout.addWidget(self.header_label,         0, 0, 1, 4)
        layout.addWidget(self.content_label_show,   0, 4, 5, 2)
        layout.addWidget(self.content_label_name,   1, 0, 1, 1)
        layout.addWidget(self.editor_label_name,    1, 1, 1, 2)
        layout.addWidget(self.button_query,         1, 3, 1, 1)
        layout.addWidget(self.button_del,           5, 4, 1, 2)
        
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 6)
        layout.setColumnStretch(3, 6)
        layout.setColumnStretch(4, 6)
        layout.setColumnStretch(5, 6)

        self.setLayout(layout)
        
    def setting_content_label(self):
        self.header_label = LabelComponent(20, "Del Student")
        self.content_label_name = LabelComponent(16, "Name: ")
        self.content_label_show = LabelComponent(16, "")
        self.content_label_show.setStyleSheet("color: red;")
    
    def setting_editor_label(self):
        self.editor_label_name = LineEditComponent("Name")

        self.editor_label_name.mousePressEvent = self.click_editor_name

        self.editor_label_name.textChanged.connect(self.enable_btn_query)
    
    def setting_button(self):
        self.button_query = ButtonComponent("Query")
        self.button_del = ButtonComponent("Delete")

        self.button_query.setEnabled(False)
        self.button_del.setEnabled(False)

        self.button_query.clicked.connect(self.click_btn_query)
        self.button_del.clicked.connect(self.click_btn_del)
    
    def load(self):
        print("delete widget")
        self.reset()
        
    def click_editor_name(self, event):
        self.editor_label_name.clear()
        self.button_del.setEnabled(False)
        
    def enable_btn_query(self):
        if self.editor_label_name.text().strip():
            self.button_query.setEnabled(True)
        else:
            self.button_query.setEnabled(False)
            
    def click_btn_query(self):
        self.query = ExecuteCommand(self.socket, 'query', self.editor_label_name.text())
        self.query.start()
        self.query.return_sig.connect(self.process_query)
        
    def click_btn_del(self):
        self.delete = ExecuteCommand(self.socket, 'delete', {'name': self.editor_label_name.text()})
        self.delete.start()
        self.reset()
        self.content_label_show.setText(f"Del {self.editor_label_name.text()} success")
        
    def process_query(self, result_dict):
        result_dict = json.loads(result_dict)
        if result_dict['status'] == 'Fail':
            self.content_label_show.setText(f"The name {self.editor_label_name.text()} is not found")
            self.editor_label_name.clear()
        else:
            self.content_label_show.setText(f"{result_dict['scores']}")
            self.button_del.setEnabled(True)

    def reset(self):
        self.content_label_show.clear()
        self.editor_label_name.setEnabled(True)
        self.editor_label_name.clear()
        self.button_del.setEnabled(False)