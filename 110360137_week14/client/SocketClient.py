import socket
import json

BUFFER_SIZE = 1940

class SocketClient:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        if not hasattr(self, 'initialized'):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.initialized = True 
        
    def send_command(self, command, student_dict):
        send_data = {'command': command, 'parameters': student_dict}
        self.client_socket.send(json.dumps(send_data).encode())
        print(f"The client sent data => {send_data}")

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(f"The client received data => {raw_data}")
        if raw_data == "closing":
            return False
        return json.loads(raw_data)
