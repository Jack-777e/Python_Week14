from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
from SocketClient import SocketClient
import json

class ExecuteCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, client:SocketClient, command, student_dict):
        super().__init__()
        self.client = client
        self.command = command
        self.student_dict = student_dict

    def run(self):
        self.client.send_command(self.command, self.student_dict)
        result_dict = self.client.wait_response()
        self.return_sig.emit(json.dumps(result_dict))
