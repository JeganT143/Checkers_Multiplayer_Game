import socket
import pickle

class Network():
    def __init__(self):
        self.client_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.msg = self.connect()

    def connect(self):
        try:
            self.client_sck.connect((self.server, self.port))
            return pickle.loads(self.client_sck.recv(2048))
        except socket.error as e:
            print(e)
        
    def get_msg(self):
        return self.msg
    
    def send(self, data):
        try:
            self.client_sck.send(pickle.dumps(data))
            msg = pickle.loads(self.client_sck.recv(2048))
            print(f"Msg received from server {msg}")
            return msg
        except socket.error as e:
            print(e)
