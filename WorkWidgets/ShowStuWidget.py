from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.SocketClient import SocketClient
import sys

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        layout.addWidget(header_label, stretch=1)
        self.setLayout(layout)
        
        self.text_list = QtWidgets.QPlainTextEdit(self)
        self.text_list.setEnabled(False)
        self.text_list.setPlainText("First init")
        layout.addWidget(self.text_list, stretch=5)
        self.setLayout(layout)
        
        self.socket_client = SocketClient("127.0.0.1", 20001)

    def load(self):
        print("show widget")
        command = "show"
        parameters = {}
        self.socket_client.send_command(command, parameters)
        status, raw_data_dict = self.socket_client.wait_response()
        print(raw_data_dict)
        self.update_text_list(raw_data_dict)
        self.text_list.setEnabled(True)

    def update_text_list(self, raw_data_dict):
        if raw_data_dict["status"] == "OK":
            parameters = raw_data_dict.get("parameters", {})
            student_list_str = "\n==== Student List ====\n"
            if not parameters:
                student_list_str += "No student data available.\n"
            else:
                for name, info in parameters.items():
                    student_list_str += f"\nName: {name}\n"
                    if "scores" in info:
                        scores = info["scores"]
                        for subject, score in scores.items():
                            student_list_str += f" Subject: {subject}, Score: {score}\n"
                    else:
                        student_list_str += " No scores found for this student.\n"
            student_list_str += "\n======================\n"
        else:
            student_list_str = "Failed to retrieve student data."

        self.text_list.setPlainText(student_list_str)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ShowStuWidget()
    main_widget.show()
    sys.exit(app.exec())
