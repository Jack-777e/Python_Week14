from threading import Thread
import socket
import json
from DBConnection import DBConnection
from DBInitializer import DBInitializer
from ServerAddStu import ServerAddStu
from ServerDelStu import ServerDelStu
from ServerModifyStu import ServerModifyStu
from ServerPrintAll import ServerPrintAll
from ServerQueryStu import ServerQueryStu
host = "127.0.0.1"
port = 20001

action_list = {
    "add": ServerAddStu,
    "del": ServerDelStu,
    "modify":ServerModifyStu,
    "query":ServerQueryStu,
    "show": ServerPrintAll
}


class SocketServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        DBConnection.db_file_path = "example.db"
        DBInitializer().execute()

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection,address=address)


    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
                kwargs={"connection": connection,"address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                print("Exeption happened {}, {}".format(e, address))
                keep_going = False
            else:
                if not message:
                    keep_going = False
                else:
                    message = json.loads(message)
                    if message['command'] == "close":
                        connection.send("closing".encode())
                        keep_going = False
                    else:
                        print(message)
                        print(f"    server received: {message} from {format(address)}")
                        reply_msg = action_list[message['command']]().execute(message)
                        connection.send(json.dumps(reply_msg).encode())
        
        connection.close()
        print("{} close connection".format(address))


if __name__ == '__main__':
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
        
    
    server.server_socket.close()
    print("leaving ....... ")
