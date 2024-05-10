import logging
import pickle
import socket
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)

class Server:
    def __init__(self, host='127.0.0.1', port=5500):
        self.HOST = host
        self.PORT = port
        # Create a TCP/IP socket
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reuse the socket even if it's recently closed
        self.SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the port
        self.SERVER.bind((self.HOST, self.PORT))
        # Dictionary to store connected clients
        self.CLIENTS = {}

    def handle_client(self, client_socket):
        while True:
            # Receive data from the client
            msg = client_socket.recv(1024)

            # If no data is received, break the loop
            if not msg:
                break

            try:
                # Deserialize the data
                msg = pickle.loads(msg)
                if isinstance(msg, tuple):
                    # If the message is a login packet ("LP"), store the client's username and password
                    if msg[0] == "LP":
                        self.CLIENTS[client_socket] = [msg[1], msg[2]]
                    # If the message is a regular message ("MSG"), send it to all clients
                    if msg[0] == "MSG":
                        self.sendAllClients(msg, client_socket)

            except Exception as e:
                # If an error occurs, print it and break the loop
                logging.error('ERROR: ' + str(e))
                break

    def sendAllClients(self, msg, sender_socket):
        # Send a message to all connected clients
        for client_socket in self.CLIENTS:
            try:
                client_socket.send(pickle.dumps(msg))
            except Exception as e:
                # If an error occurs, print it and remove the client from the list of connected clients
                logging.error(f"Error sending to client: {e}")
                del self.CLIENTS[client_socket]

    def start_server(self):
        # Start listening for incoming connections
        self.SERVER.listen()
        logging.info(f'## START SERVER -|-')
        logging.info(f'Listening on {self.HOST}:{self.PORT}')

        while True:
            # Accept a new connection
            client_socket, addr = self.SERVER.accept()
            logging.info(f'Connection established with {addr}')

            # Start a new thread to handle the client
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()

# Create a new server
server = Server()
# Start the server in a new thread
server_thread = threading.Thread(target=server.start_server)
server_thread.start()
