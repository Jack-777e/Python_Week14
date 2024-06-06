from PyQt6 import QtWidgets
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.SocketClient import SocketClient
from client.PrintAll import PrintAll

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.socket_client = SocketClient("127.0.0.1", 20001)

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(22, "成績列表")
        header_label.setStyleSheet("color: lightgreen")

        layout.addWidget(header_label, stretch=1)
        self.setLayout(layout)
        
        Form = QtWidgets.QWidget()

        self.text_list = QtWidgets.QPlainTextEdit(Form)  # QPlainTextEdit 多行輸入框
        self.text_list.setGeometry(20, 130, 200, 100)
        self.text_list.setEnabled(False)
        self.text_list.setPlainText("First init")
        layout.addWidget(self.text_list, stretch=8)
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
            student_list_str = "==== 成績列表 ====\n"
            if not data:
                student_list_str += "沒有任何成績資料\n"
            else:
                for name, scores in data.items():
                    student_list_str += f"\n姓名: {name}\n"
                    for subject, score in scores['scores'].items():
                        student_list_str += f" 科目: {subject}, 成績: {score}\n"
                
            student_list_str += "\n================\n"
        else:
            student_list_str = "無法取得成績資料"

        self.text_list.setPlainText(student_list_str)
