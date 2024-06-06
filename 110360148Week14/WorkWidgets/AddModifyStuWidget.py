from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import *
from ExecuteCommand import ExecuteCommand
import json


class AddModifyStuWidget(QtWidgets.QWidget):
    def __init__(self, socket):
        super().__init__()
        self.setObjectName("add_modify_stu_widget")
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
        layout.addWidget(self.content_label_subject,2, 0, 1, 1)
        layout.addWidget(self.editor_label_subject, 2, 1, 1, 2)
        layout.addWidget(self.content_label_score,  3, 0, 1, 1)
        layout.addWidget(self.editor_label_score,   3, 1, 1, 2)
        layout.addWidget(self.button_add,           3, 3, 1, 1)
        layout.addWidget(self.button_send_modify,   5, 4, 1, 2)
        
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 6)
        layout.setColumnStretch(3, 6)
        layout.setColumnStretch(4, 6)
        layout.setColumnStretch(5, 6)

        self.setLayout(layout)

    def setting_content_label(self):
        self.header_label = LabelComponent(20, "Add / Modify Student")
        self.content_label_name = LabelComponent(16, "Name: ")
        self.content_label_subject = LabelComponent(16, "Subject: ")
        self.content_label_score = LabelComponent(16, "Score: ")
        self.content_label_show = LabelComponent(16, "")
        self.content_label_show.setStyleSheet("color: red;")
        
    def setting_editor_label(self):
        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_subject = ComboBoxComponent()
        self.editor_label_score = LineEditComponent("Score")

        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setEnabled(False)
        self.editor_label_score.setValidator(QtGui.QIntValidator(0, 100))

        self.editor_label_name.mousePressEvent = self.clear_editor_name
        self.editor_label_score.mousePressEvent = self.clear_editor_score

        self.editor_label_name.textChanged.connect(self.enable_btn_query)
        self.editor_label_subject.lineEdit().textChanged.connect(self.enable_btn_add_modify)
        self.editor_label_subject.lineEdit().textChanged.connect(self.set_editor_score)
        self.editor_label_score.textChanged.connect(self.enable_btn_add_modify)
        
    def setting_button(self):
        self.button_query = ButtonComponent("Query")
        self.button_add = ButtonComponent("Add")
        self.button_send_modify = ButtonComponent("Send")

        self.button_query.setEnabled(False)
        self.button_add.setEnabled(False)
        self.button_send_modify.setEnabled(False)

        self.button_query.clicked.connect(self.click_btn_query)
        self.button_add.clicked.connect(self.click_btn_add)
        self.button_send_modify.clicked.connect(self.click_btn_modify)
        
    def load(self):
        self.reset()
        print("add / modify widget")
        
    def clear_editor_name(self, event):
        self.editor_label_name.clear()

    def clear_editor_score(self, event):
        self.editor_label_score.clear()
        
    def enable_btn_query(self):
        if self.editor_label_name.text().strip():
            self.button_query.setEnabled(True)
        else:
            self.button_query.setEnabled(False)
    
    def enable_btn_add_modify(self):
        if self.editor_label_subject.lineEdit().text().strip() and self.editor_label_score.text().strip():
            if self.is_add:
                self.button_add.setEnabled(True)
            else:
                self.button_send_modify.setEnabled(True)
        else:
            if self.is_add:
                self.button_add.setEnabled(False)
            else:
                self.button_send_modify.setEnabled(False)
            
    def set_editor_score(self):
        try:
            self.editor_label_score.setText(str(self.student_dict['scores_dict'][self.editor_label_subject.currentText()]))
        except:
            self.editor_label_score.setText("")
    
    def click_btn_query(self):
        self.query = ExecuteCommand(self.socket, 'query', self.editor_label_name.text())
        self.query.start()
        self.query.return_sig.connect(self.process_query)
        
    def click_btn_add(self):
        self.button_send_modify.setEnabled(True)
        self.student_dict['scores'][self.editor_label_subject.currentText()] = self.editor_label_score.text()
        self.content_label_show.setText(f"Student {self.editor_label_name.text()}'s subject '{self.editor_label_subject.currentText()}' with score '{self.editor_label_score.text()}' added")
        
    def click_btn_send(self):
        self.send = ExecuteCommand(self.socket, 'add', self.student_dict)
        self.send.start()
        self.reset()
        self.content_label_show.setText(f"Add {self.student_dict} success")
    
    def click_btn_modify(self):
        self.student_dict['scores_dict'][self.editor_label_subject.currentText()] = self.editor_label_score.text()
        self.send = ExecuteCommand(self.socket, 'modify', self.student_dict)
        self.send.start()
        self.reset()
        self.content_label_show.setText(f"Modify {self.student_dict['name']}'s scores success")
    
    def process_query(self, result_dict):
        result_dict = json.loads(result_dict)

        if result_dict['status'] == 'OK':
            self.is_add = False
            self.student_dict = {'name': self.editor_label_name.text(), 'scores_dict': result_dict['scores']}
            self.editor_label_subject.addItems(self.student_dict['scores_dict'].keys())
            self.content_label_show.setText("Please select a subject or new a subject")
            self.button_send_modify.setText("Modify")
            self.button_send_modify.clicked.disconnect()
            self.button_send_modify.clicked.connect(self.click_btn_modify)
        else:
            self.is_add = True
            self.student_dict = {'name': self.editor_label_name.text(), 'scores' : {}}
            self.content_label_show.setText(f"Please enter subjects for student '{self.editor_label_name.text()}'")
            self.button_send_modify.setText("Send")
            self.button_send_modify.clicked.disconnect()
            self.button_send_modify.clicked.connect(self.click_btn_send)
            
        self.editor_label_name.setEnabled(False)
        self.editor_label_subject.setEnabled(True)
        self.editor_label_score.setEnabled(True)
        self.button_query.setEnabled(False)

    def reset(self):
        self.content_label_show.clear()
        self.editor_label_name.clear()
        self.editor_label_subject.clear()
        self.editor_label_subject.lineEdit().clear()
        self.editor_label_score.clear()
        self.editor_label_name.setEnabled(True)
        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setEnabled(False)
        self.button_send_modify.setEnabled(False)