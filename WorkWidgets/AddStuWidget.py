from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.SocketClient import SocketClient
import json

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.student_dict = dict()
        self.socket_client = SocketClient("127.0.0.1", 20001)
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        self.message_label = LabelComponent(14, " ")
        self.message_label.setStyleSheet("color: red")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(15, "Subject: ")
        score_label = LabelComponent(15, "Score: ")

        self.name_editor_label = LineEditComponent(placeholder_text= "name")
        self.subject_editor_label = LineEditComponent(placeholder_text= "Subject")
        self.score_editor_label = LineEditComponent(placeholder_text="Score")
        
        # 設置 Validators
        english_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z ]+"), self)  
        numeric_validator = QtGui.QIntValidator(0, 100, self) 

        # 將 Validators 連接到 LineEdit
        self.name_editor_label.setValidator(english_validator)
        self.subject_editor_label.setValidator(english_validator)
        self.score_editor_label.setValidator(numeric_validator) 

        self.query_button = ButtonComponent("Query")
        self.add_button = ButtonComponent("Add")
        self.send_button = ButtonComponent("Send")

        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
        
        self.name_editor_label.mousePressEvent = self.clear_name_editor
        self.subject_editor_label.mousePressEvent = self.clear_subject_editor
        self.score_editor_label.mousePressEvent = self.clear_score_editor
        
        self.name_editor_label.textChanged.connect(self.on_name_changed)
        self.query_button.clicked.connect(self.name_query)
        self.subject_editor_label.textChanged.connect(self.enable_add_button)
        self.score_editor_label.textChanged.connect(self.enable_add_button)
        self.add_button.clicked.connect(self.enable_send_button)
        self.send_button.clicked.connect(self.confirm_action)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.message_label, 0, 3, 3, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_editor_label, 1, 1, 1, 1)
        layout.addWidget(self.query_button, 1, 2, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 1)
        layout.addWidget(self.add_button, 3, 2, 1, 1)
        layout.addWidget(self.send_button, 4, 3, 2, 1)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 4)

        layout.setRowStretch(0, 3)
        layout.setRowStretch(1, 3)
        layout.setRowStretch(2, 3)
        layout.setRowStretch(3, 3)
        layout.setRowStretch(4, 3)
        layout.setRowStretch(5, 3)

        self.setLayout(layout)

    def clear_name_editor(self, event):
        self.name_editor_label.clear()

    def clear_subject_editor(self, event):
        self.subject_editor_label.clear()

    def clear_score_editor(self, event):
        self.score_editor_label.clear()
        
    def on_name_changed(self):
        if self.name_editor_label.text().strip():
            self.query_button.setEnabled(True)
        else:
            self.query_button.setEnabled(False)

    def name_query(self):
        name = self.name_editor_label.text().strip()
        command = "query"
        parameters = {}
        parameters['name']=name
        self.socket_client.send_command(command,parameters)
        status,raw_data_dict=self.socket_client.wait_response()
        
        if (raw_data_dict['status']=="OK") :
            print("Student already exist.")
        else:
            self.enable_subject_score_lab()


    def enable_subject_score_lab(self):
        name = self.name_editor_label.text().strip()
        self.student_dict = {'name' : name, 'scores' : {}}
        if name:
            self.message_label.setText(f"Please input subject for student '{name}'")
        else:
            self.message_label.setText("")
        self.query_button.setEnabled(False)
        self.name_editor_label.setEnabled(False)
        self.subject_editor_label.setEnabled(True)
        self.score_editor_label.setEnabled(True)
        
    def enable_add_button(self):
        if self.subject_editor_label.text().strip() and self.score_editor_label.text().strip():
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def enable_send_button(self):
        subject = self.subject_editor_label.text().strip()
        score = self.score_editor_label.text().strip()
        name = self.student_dict["name"]
        self.student_dict["scores"][subject] = score
        self.send_button.setEnabled(True)
        self.message_label.setText(f"Student {name}'s subject and scores added")
        
    def confirm_action(self):
        command = "add"
        self.socket_client.send_command(command,self.student_dict)
        status,raw_data_dict=self.socket_client.wait_response()
        if status:
            name = self.student_dict["name"]
            self.message_label.setText(f"Student {name}'s subject and scores sended")
            self.reset_to_initial_state()
    
    def reset_to_initial_state(self):
        self.name_editor_label.clear()
        self.subject_editor_label.clear()
        self.score_editor_label.clear()

        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)

        self.name_editor_label.setEnabled(True)
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)

        self.student_dict={}

    def load(self):
        print("add widget")
