import socket
import pickle


class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pnumber = self.connect()

    def getplayerID(self):
        return self.pnumber

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2000))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2000))
        except socket.error as e:
            print(e)
