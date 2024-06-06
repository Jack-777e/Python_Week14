from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import *
from ExecuteCommand import ExecuteCommand
import json

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self, socket):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.socket = socket
        
        layout = QtWidgets.QVBoxLayout()

        self.header_label = LabelComponent(20, "Show Student")
        # self.list_view = ListWidgetComponent()    #ListWidget
        self.text_edit = TextEditComponent()    #TextEdit
        self.text_edit.setReadOnly(True)    #TextEdit

        layout.addWidget(self.header_label, 10)
        # layout.addWidget(self.list_view, 90)  #ListWidget
        layout.addWidget(self.text_edit, 90)

        self.setLayout(layout)
        
    def load(self):
        print("show widget")
        # self.list_view.clear()    #ListWidget
        self.print_all = ExecuteCommand(self.socket, 'show', {})
        self.print_all.start()
        self.print_all.return_sig.connect(self.process_print_all)
    
    def process_print_all(self, result_dict):
        result_dict = json.loads(result_dict)
        student_dict = result_dict['parameters']
        # # # ListWidget
        # self.list_view.addItem("====== student list ======\n")
        # for name in student_dict.keys():
        #     self.list_view.set.addItem(f"Name: {name}")
        #     for subject, score in student_dict[name]['scores'].items():
        #         self.list_view.addItem(f"  subject: {subject}, score: {score}")
        #     self.list_view.addItem("")
        # self.list_view.addItem("======================")
        
        # # # TextEdit
        student_dict_text = "====== student list ======\n"
        for name in student_dict.keys():
            student_dict_text += f"Name: {name}\n"
            for subject, score in student_dict[name]['scores'].items():
                student_dict_text += f"  subject: {subject}, score: {score}\n"
            student_dict_text += "\n"
        student_dict_text += "====================="
        self.text_edit.setPlainText(student_dict_text)