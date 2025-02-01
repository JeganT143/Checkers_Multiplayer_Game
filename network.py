import socket
import pickle     # used to send python objects to be sent over the network

class Network():
    def __init__(self):
        self.client_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creates a TCP socket
        self.server = socket.gethostbyname(socket.gethostname())  # gets IP address of the machine running the client side
        self.port = 5050                         
        self.msg = self.connect()

    def connect(self):
        try:
            self.client_sck.connect((self.server, self.port))         # connects to server using IP address
            return pickle.loads(self.client_sck.recv(2048))            
        except socket.error as e:
            print(e)
        
    def get_msg(self):
        return self.msg
    
    def send(self, data):
        try:
            self.client_sck.send(pickle.dumps(data))      # data is sent using pickle.dump 
            msg = pickle.loads(self.client_sck.recv(2048))    # data is received with pickle.loads
            print(f"Msg received from server {msg}")
            return msg
        except socket.error as e:
            print(e)
