from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from WorkWidgets.SocketClient import SocketClient
import time

class DeleteStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.student_dict = dict()
        self.socket_client = SocketClient("127.0.0.1", 20001)
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Delete Student")
        self.message_label = LabelComponent(14, " ")
        self.message_label.setStyleSheet("color: red")
        name_label = LabelComponent(16, "Name: ")

        self.name_list_label = ComboBoxComponent()


        self.delete_button = ButtonComponent("Delete")

        self.delete_button.clicked.connect(self.confirm_action)
        self.reset_to_initial_state()

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.message_label, 0, 3, 3, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_list_label, 1, 1, 1, 1)
        layout.addWidget(self.delete_button, 4, 3, 3, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 3)

        self.setLayout(layout)

    def confirm_action(self):
        name = self.name_list_label.currentText()
        new_student_dict = {'name' : name}
        self.socket_client.send_command("del",new_student_dict)
        status,raw_data_dict=self.socket_client.wait_response()
        if raw_data_dict["status"] == "OK":
            self.message_label.setText("Delete successful")
        else:
            self.message_label.setText("Delete failed")
        
        
        self.reset_to_initial_state()


    def reset_to_initial_state(self):
        self.name_list_label.clear()
        self.name_list_label.setEnabled(True)
        self.get_name_list()


    def load(self):
        print("modify widget")
        self.name_list_label.clear()
        self.get_name_list()


    def get_name_list(self):
        self.student_dict = {'name': {}}
        self.socket_client.send_command("show",self.student_dict)
        status,raw_data_dict=self.socket_client.wait_response()
        
        if raw_data_dict['status'] == "OK":
            self.name_list_label.addItems(raw_data_dict['parameters'].keys())
        else:
            self.message_label.setText("Can't get the student list")
            self.reset_to_initial_state()
        
        name=self.name_list_label.currentText()
        if(name == ""):
            self.delete_button.setEnabled(False)
            self.message_label.setText("No student information")
        else :
            self.delete_button.setEnabled(True)
            self.message_label.setText("Obtain student information successfully")





"""
的結果為dict_keys(['asdawd', 'asdwad', 'wdadad', 'a', 'b'])
原始資料{'status': 'OK', 'parameters': {'asdawd': {'name': 'asdawd', 'scores': {'naolsdfk': 414.0}}, 'asdwad': {'name': 'asdwad', 'scores': {'wadg': 488.0}}, 'wdadad': {'name': 'wdadad', 'scores': {'aaaaaa': 87.0, 'awaa': 87.0}}, 'a': {'name': 'a', 'scores': {'a': 2.0, 'b': 1.0, 'c': 1.0, 'd': 1.0, 'e': 24.0}}, 'b': 
{'name': 'b', 'scores': {'a': 2.0, 'b': 2.0}}}}
如何正確提取裡面的資料

"""


