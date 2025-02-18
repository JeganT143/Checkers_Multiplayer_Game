import socket
import pickle
import pygame


class Network():
    def __init__(self, server_ip=None):
        self.client_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        # self.server = "10.50.60.110"
        self.port = 5050
        self.p = self.connect()
        self.select_sound = pygame.mixer.Sound("select.wav")
        self.move_sound = pygame.mixer.Sound("move.wav")
        
    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client_sck.connect((self.server, self.port))
            # The server sends the player's number as a string.
            return int(self.client_sck.recv(2048).decode())
        except socket.error as e:
            print(e)
    
    def send(self, data):
        try:
            if isinstance(data, str):
                self.client_sck.send(data.encode())
            else:
                self.client_sck.send(pickle.dumps(data))
            response = self.client_sck.recv(2048)
            try:
                return pickle.loads(response)
            except Exception:
                return response.decode()
        except socket.error as e:
            print(e)
