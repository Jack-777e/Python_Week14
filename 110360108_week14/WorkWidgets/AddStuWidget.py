from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.SocketClient import SocketClient
from client.Query import Query
from client.AddStu import AddStu

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.student_dict = dict()
        self.socket_client = SocketClient("127.0.0.1", 20001)

        self.setStyleSheet("""
            QWidget#add_stu_widget {
                background-color: #e0f7fa;
            }
            QLabel {
                color: #00796b;
            }
            QLineEdit {
                border: 2px solid #00796b;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #00796b;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #004d40;
            }
        """)

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        self.message_label = LabelComponent(14, " ")
        self.message_label.setStyleSheet("color: red")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(15, "Subject: ")
        score_label = LabelComponent(15, "Score: ")

        self.name_editor_label = LineEditComponent(default_content="name")
        self.subject_editor_label = LineEditComponent(placeholder_text="Subject")
        self.score_editor_label = LineEditComponent(placeholder_text="Score")

        english_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z ]+"), self)  
        numeric_validator = QtGui.QIntValidator(0, 100, self) 

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
        self.query_button.clicked.connect(self.enable_subject_score_lab)
        self.subject_editor_label.textChanged.connect(self.enable_add_button)
        self.score_editor_label.textChanged.connect(self.enable_add_button)
        self.send_button.clicked.connect(self.confirm_action)
        self.add_button.clicked.connect(self.enable_send_button)

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
        layout.addWidget(self.send_button, 4, 3, 3, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 3)

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

    def enable_subject_score_lab(self):
        name = self.name_editor_label.text().strip()
        self.student_dict = {'name': name, 'scores': {}} 
        Query.execute(self.socket_client, name)

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
        self.message_label.setText(f"Student {name}'s subject '{subject}' with score '{score}' added")
        self.raw_data = AddStu.execute(self.socket_client, self.student_dict)
        self.send_button.setEnabled(True)

    def confirm_action(self):
        self.message_label.setText(f"The information {self.student_dict} is sent")
        print(f"Add {self.student_dict} {'success' if self.raw_data['status'] == 'OK' else 'Fail'}")
        self.reset_to_initial_state()

    def reset_to_initial_state(self):
        self.name_editor_label.clear()
        self.subject_editor_label.clear()
        self.score_editor_label.clear()

        self.name_editor_label.setEnabled(True)
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)

        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)

    def load(self):
        print("add widget")
