from tkinter import *
from window import LoginWindow, Window
from client import Client
import logging

def app():
    # Create a client
    client = Client()
    try:
        # Try to connect to the server
        client.connect()
    except Exception as e:
        # If an error occurs, log it
        logging.info(e)
    # Create a login window
    logWin = LoginWindow(client)
    # If the user is registered, create a chat window
    if logWin.isRegister == True:
        chatWin = Window(client)

if __name__ == '__main__':
    app()
