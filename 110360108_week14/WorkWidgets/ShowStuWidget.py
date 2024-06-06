from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.SocketClient import SocketClient
from client.PrintAll import PrintAll

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.socket_client = SocketClient("127.0.0.1", 20001)

        self.setStyleSheet("""
            QWidget#show_stu_widget {
                background-color: #e8f5e9;
            }
            QLabel {
                color: #388e3c;
            }
            QPlainTextEdit {
                border: 2px solid #388e3c;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: #ffffff;
                color: #388e3c;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")

        layout.addWidget(header_label, stretch=1)
        self.setLayout(layout)

        Form = QtWidgets.QWidget()

        self.text_list = QtWidgets.QPlainTextEdit(Form)
        self.text_list.setGeometry(20, 130, 200, 100)
        self.text_list.setEnabled(False)
        self.text_list.setPlainText("First init")
        layout.addWidget(self.text_list, stretch=5)
        self.setLayout(layout)

        Form.show()

        
    def load(self):
        print("show widget")
        raw_data = PrintAll.execute(self.socket_client)
        
        self.update_text_list(raw_data)
        self.text_list.setEnabled(True)

    def update_text_list(self, raw_data):
        data = raw_data['parameters']
        
        if raw_data["status"] == "OK":
            student_list_str = "==== student list ====\n"
            if not data:
                student_list_str += "No student data available.\n"
            else:
                for name, scores in data.items():
                    student_list_str += f"\nName: {name}\n"
                    for subject, score in scores['scores'].items():
                        student_list_str += f" Subject: {subject}, Score: {score}\n"
                
            student_list_str += "\n================\n"
        else:
            student_list_str = "Failed to retrieve student data."

        self.text_list.setPlainText(student_list_str)
