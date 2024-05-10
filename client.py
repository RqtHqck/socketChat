import socket
import logging
import pickle
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)

class Client:
    def __init__(self, host='127.0.0.1', port=5500):
        self.HOST = host
        self.PORT = port
        # Create a TCP/IP socket
        self.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Initialize username and password
        self.username = None
        self.password = None

    def connect(self):
        # Connect to the server
        try:
            self.CLIENT_SOCKET.connect((self.HOST, self.PORT))
            logging.info(f'Connected to server at {self.HOST}:{self.PORT}')
        except Exception as e:
            logging.error(e)


    def login(self, username, password):
        # Store the username and password
        self.username = username
        self.password = password
        return True

    def SendMsg(self, msg):
        # Serialize the message and send it to the server
        try:
            serialized_msg = pickle.dumps(msg)
            self.CLIENT_SOCKET.sendall(serialized_msg)
        except Exception as e:
            logging.error(e)

    def receive_msg(self):
        while True:
            # Receive messages from the server
            data = self.CLIENT_SOCKET.recv(1024)
            msg = pickle.loads(data)
            # If a message is received, return it
            if msg:
                return msg
