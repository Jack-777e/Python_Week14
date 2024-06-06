from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.SocketClient import SocketClient
from client.Query import Query
from client.DelStu import DelStu

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("del_stu_widget")
        self.socket_client = SocketClient("127.0.0.1", 20001)
        self.student_dict = dict()
        
        self.setStyleSheet("""
            QWidget#del_stu_widget {
                background-color: #ffebee;
            }
            QLabel {
                color: #d32f2f;
            }
            QLineEdit {
                border: 2px solid #d32f2f;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPlainTextEdit {
                border: 2px solid #d32f2f;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: #ffffff;
                color: #d32f2f;
            }
        """)

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Del Student")
    
        
        name_label = LabelComponent(16, "Name: ")
        
        self.name_editor_label = LineEditComponent(default_content="name")
        
        english_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z ]+"), self)
        self.name_editor_label.setValidator(english_validator)
        
        self.query_button = ButtonComponent("Query")
        self.query_button.setEnabled(False)
        
        self.confirm_button = ButtonComponent("Confirm")
        self.confirm_button.setEnabled(False)
        
        self.cancle_button = ButtonComponent("Cancel")
        self.cancle_button.setEnabled(False)
        
        self.name_editor_label.mousePressEvent = self.clear_name_editor
        
        self.name_editor_label.textChanged.connect(self.on_name_changed)
        self.query_button.clicked.connect(self.print_student_info)
        self.confirm_button.clicked.connect(self.confirm_action)
        self.cancle_button.clicked.connect(self.cancle_action)
        
        Form = QtWidgets.QWidget()

        self.text_list = QtWidgets.QPlainTextEdit(Form)
        self.text_list.setGeometry(20, 130, 200, 100)
        self.text_list.setEnabled(False)

        Form.show()
        
        layout.addWidget(header_label,              0, 0, 1, 2)
        layout.addWidget(name_label,                1, 0, 1, 1)
        layout.addWidget(self.name_editor_label,    1, 1, 1, 1)
        layout.addWidget(self.query_button,         1, 2, 1, 1)
        layout.addWidget(self.text_list,            2, 0, 3, 2)
        layout.addWidget(self.confirm_button,       3, 3, 3, 1)
        layout.addWidget(self.cancle_button,        3, 4, 3, 1)
        
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 4)
        
        self.setLayout(layout)
        
    def clear_name_editor(self, event):
        self.name_editor_label.clear()
    
    def on_name_changed(self):
        if self.name_editor_label.text().strip():
            self.query_button.setEnabled(True)
        else:
            self.query_button.setEnabled(False)
            self.confirm_button.setEnabled(False)
            self.cancle_button.setEnabled(False)
    
    def enable_confirm_and_cancle_button(self):
        self.confirm_button.setEnabled(True)
        self.cancle_button.setEnabled(True)
    
    def print_student_info(self):
        name = self.name_editor_label.text().strip()
        self.student_dict = {'name': name, 'scores': {}} 
        status, scores = Query.execute(self.socket_client, name)
        
        if status == "OK":
            self.update_text_list(scores)
            self.enable_confirm_and_cancle_button()
        else:
            self.update_text_list(scores)
            self.reset_to_initial_state()
            
    def confirm_action(self):
        name = self.name_editor_label.text().strip()
        raw_data = DelStu.execute(self.socket_client, self.student_dict)
        print(f"delete {name} {'success' if raw_data['status'] == 'OK' else 'Fail'}")
        self.text_list.setPlainText(f"delete {name} {'success' if raw_data['status'] == 'OK' else 'Fail'}")
        
        self.reset_to_initial_state()
        
    def cancle_action(self):
        self.reset_to_initial_state()
    
    def load(self):
        print("del widget")
        
    def update_text_list(self, scores):
        name = self.student_dict["name"]
        if scores is None or not scores:
            student_list_str = "The Student not found"
            
        else:
            student_list_str = f"{name}'s list\n"
            for subject, score in scores.items():
                student_list_str += f"Subject: {subject}, Score: {score}\n"
            

        self.text_list.setPlainText(student_list_str)
        
    def reset_to_initial_state(self):
        self.name_editor_label.clear()
        self.name_editor_label.setEnabled(True)
        self.query_button.setEnabled(False)
        self.confirm_button.setEnabled(False)
        self.cancle_button.setEnabled(False)

