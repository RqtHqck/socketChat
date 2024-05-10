import time
from tkinter import *
from tkinter import messagebox
import logging
import pickle
import threading

class LoginWindow:
    def __init__(self, client):
        # Set up logging for the authentication process
        logging.info(f'-- AUTHENTICATION PROCESS... --')
        self.window = Tk()
        self.isRegister = False

        # Initialize username and password
        self.username = StringVar()
        self.password = StringVar()
        self.CLIENT = client

        # Create login form
        Label(self.window, text='Username:').pack()
        Entry(self.window, textvariable=self.username).pack()
        Label(self.window, text='Password:').pack()
        Entry(self.window, textvariable=self.password, show='*').pack()
        Button(self.window, text='Login', command=self.loginValidation).pack()

        self.window.mainloop()

    def loginValidation(self):
        # Validate login credentials
        username = self.username.get()
        password = self.password.get()

        if self.CLIENT.login(username, password):
            # If login is successful, send a login packet to the server
            messagebox.showinfo('Success', 'Logged in successfully!')
            data = ('LP', username, password)
            try:
                self.CLIENT.SendMsg(data)
                self.isRegister = True

                # Close the login window
                self.window.destroy()
            except Exception as e:
                logging.error(e)
        else:
            # If login is unsuccessful, show an error message
            messagebox.showerror('Error', 'Invalid username or password')
            self.window.destroy()


class Window:
    def __init__(self, client):
        self.window = Tk()

        # Initialize text and username
        self.text = StringVar()
        self.username = StringVar()
        self.CLIENT = client

        # Set up chat window
        self.username.set(client.username)
        self.text.set('')
        self.window.title('CHAT')
        self.window.geometry('400x600')

        # Create chat log, username entry, and message entry
        self.log = Text(self.window, )
        self.log.config(state='disabled')
        self.nick = Entry(self.window, textvariable=self.username)
        self.msg = Entry(self.window, textvariable=self.text)

        # Create send button
        self.send_button = Button(self.window, text='Send', command=self.sendMessage)

        # Pack widgets
        self.send_button.pack(side='bottom', fill='x')
        self.msg.pack(side='bottom', fill='x', expand='true')
        self.nick.pack(side='bottom', fill='x', expand='true')
        self.log.pack(side='top', fill='both', expand='true')

        # Start chat
        self.startChat()
        self.window.mainloop()

    def startChat(self):
        # Start chat process
        logging.info("-- CLIENT START CHATTING... --")
        SendMsg = ("MSG", f"Greeting new user {self.CLIENT.username}")
        try:
            self.CLIENT.SendMsg(SendMsg)
            threading.Thread(target=self.receiveMessage).start()
        except Exception as e:
            logging.error(e)

    def receiveMessage(self):
        while True:
            # Receive messages from the server
            try:
                msgFromServer = self.CLIENT.receive_msg()
                if msgFromServer:  # Check if there is a new message
                    self.log.config(state='normal')
                    self.log.insert('end', msgFromServer[1] + '\n')
                    self.log.config(state='disabled')
                time.sleep(0.1)  # Delay of 0.1 second
            except Exception as e:
                logging.error(e)

    def sendMessage(self):
        # Send message to the server
        try:
            msgToSend = self.text.get()
            userTemplate = f'<{self.CLIENT.username}>: '
            msg = ("MSG", userTemplate + msgToSend)
            self.CLIENT.SendMsg(msg)
            self.text.set('')
        except Exception as e:
            logging.error(e)
