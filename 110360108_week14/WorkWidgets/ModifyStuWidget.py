from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from client.SocketClient import SocketClient
from client.Query import Query
from client.ModifyStu import ModifyStu

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.student_dict = dict()
        self.socket_client = SocketClient("127.0.0.1", 20001)

        self.setStyleSheet("""
            QWidget#modify_stu_widget {
                background-color: #fff3e0;
            }
            QLabel {
                color: #ff8f00;
            }
            QLineEdit, QComboBox {
                border: 2px solid #ff8f00;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #ff8f00;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #e65100;
            }
        """)

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Modify Student")
        self.message_label = LabelComponent(14, " ")
        self.message_label.setStyleSheet("color: red")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(15, "Subject: ")
        score_label = LabelComponent(15, "Score: ")

        self.name_editor_label = LineEditComponent(default_content="name")
        self.subject_editor_label = ComboBoxComponent()
        self.score_editor_label = LineEditComponent(placeholder_text="Score")

        english_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z ]+"), self)
        numeric_validator = QtGui.QIntValidator(0, 100, self)

        self.name_editor_label.setValidator(english_validator)
        self.score_editor_label.setValidator(numeric_validator)

        self.query_button = ButtonComponent("Query")
        self.modify_button = ButtonComponent("Modify")

        self.reset_to_initial_state()

        self.name_editor_label.mousePressEvent = self.clear_name_editor
        self.subject_editor_label.lineEdit().mousePressEvent = self.clear_subject_editor
        self.score_editor_label.mousePressEvent = self.clear_score_editor

        self.name_editor_label.textChanged.connect(self.on_name_changed)
        self.query_button.clicked.connect(self.query_action)
        self.subject_editor_label.lineEdit().textChanged.connect(self.update_score_field)
        self.subject_editor_label.currentTextChanged.connect(self.update_score_field)
        self.score_editor_label.textChanged.connect(self.enable_modify_button)
        self.modify_button.clicked.connect(self.confirm_action)

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
        status, scores = Query.execute(self.socket_client, name)
        
        if status == "OK":
            self.student_dict['scores'] = scores
            self.subject_editor_label.clear()
            self.subject_editor_label.addItems(scores.keys())
            self.message_label.setText("Please select or add a subject to edit score.")
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
        
        self.student_dict['name'] = name
        self.student_dict['scores'][subject] = int(score)
        status = ModifyStu.execute(self.socket_client, self.student_dict)
        if status == "OK":
            self.message_label.setText("Modification successful!")
        else:
            self.message_label.setText("Modification failed!")
        
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
