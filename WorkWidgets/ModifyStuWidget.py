from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from WorkWidgets.SocketClient import SocketClient

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.student_dict = dict()
        self.socket_client = SocketClient("127.0.0.1", 20001)
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Modify Student")
        self.message_label = LabelComponent(14, " ")
        self.message_label.setStyleSheet("color: red")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(15, "Subject: ")
        score_label = LabelComponent(15, "Score: ")

        self.name_editor_label = LineEditComponent(placeholder_text= "name")
        self.subject_editor_label = LineEditComponent(placeholder_text= "Subject")
        self.score_editor_label = LineEditComponent(placeholder_text="Score")
        self.subject_editor_label = ComboBoxComponent()
        self.subject_editor_label.setEditable(True) 

        english_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z ]+"), self)
        numeric_validator = QtGui.QIntValidator(0, 100, self)

        self.name_editor_label.setValidator(english_validator)
        self.score_editor_label.setValidator(numeric_validator)

        self.query_button = ButtonComponent("Query")
        self.modify_button = ButtonComponent("Modify")

        
        self.name_editor_label.mousePressEvent = self.clear_name_editor
        self.score_editor_label.mousePressEvent = self.clear_score_editor

        self.name_editor_label.textChanged.connect(self.on_name_changed)
        self.query_button.clicked.connect(self.query_action)
        self.score_editor_label.textChanged.connect(self.enable_modify_button)
        self.modify_button.clicked.connect(self.confirm_action)
        self.reset_to_initial_state()

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.message_label, 0, 3, 3, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_editor_label, 1, 1, 1, 1)
        layout.addWidget(self.query_button, 1, 2, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 1)
        layout.addWidget(self.modify_button, 4, 3, 3, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 3)

        self.setLayout(layout)

    def clear_name_editor(self, event):
        self.name_editor_label.clear()

    def clear_subject_editor(self, event):
        self.subject_editor_label.clearEditText()

    def clear_score_editor(self, event):
        self.score_editor_label.clear()

    def on_name_changed(self):
        if self.name_editor_label.text().strip():
            self.query_button.setEnabled(True)
        else:
            self.query_button.setEnabled(False)

    def enable_subject_score_lab(self):
        self.subject_editor_label.setEnabled(True)
        self.score_editor_label.setEnabled(True)

    def query_action(self):
        name = self.name_editor_label.text().strip()
        self.student_dict = {'name': name, 'scores': {}}
        self.socket_client.send_command("query",self.student_dict)
        status,raw_data_dict=self.socket_client.wait_response()
        
        if raw_data_dict['status'] == "OK":
            self.student_dict['scores'] = raw_data_dict['scores']
            self.subject_editor_label.clear()
            self.subject_editor_label.addItems(self.student_dict['scores'].keys())
            self.message_label.setText("Please select a subject to edit, or add a subject and it's score.")
            self.enable_subject_score_lab()
        else:
            self.message_label.setText("The student not found")
            self.reset_to_initial_state()
        
    def update_score_field(self):
        subject = self.subject_editor_label.currentText().strip()
        if subject in self.student_dict['scores']:
            score = self.student_dict['scores'][subject]
            self.score_editor_label.setText(str(score))
        else:
            self.score_editor_label.clear()

    def enable_modify_button(self):
        subject = self.subject_editor_label.currentText().strip()
        score = self.score_editor_label.text().strip()
        
        if subject and score:
            self.modify_button.setEnabled(True)
        else:
            self.modify_button.setEnabled(False)

    def confirm_action(self):
        name = self.name_editor_label.text().strip()
        subject = self.subject_editor_label.currentText().strip()
        score = self.score_editor_label.text().strip()
        new_student_dict = {'name' : name, 'scores' : {}}
        new_student_dict["scores"][subject] = score
        self.socket_client.send_command("modify",new_student_dict)
        status,raw_data_dict=self.socket_client.wait_response()
        if raw_data_dict["status"] == "OK":
            self.message_label.setText("Modify successful")
        else:
            self.message_label.setText("Modify failed")
        
        self.reset_to_initial_state()

    def reset_to_initial_state(self):
        self.name_editor_label.clear()
        self.subject_editor_label.clearEditText()
        self.score_editor_label.clear()

        self.name_editor_label.setEnabled(True)
        self.query_button.setEnabled(False)
        self.modify_button.setEnabled(False)

        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)

    def load(self):
        print("modify widget")
