from tkinter import *
from tkinter import messagebox
import logging


class Win():
    def __init__(self, client):
        self.window = Tk()
        self.username = StringVar()
        self.CLIENT = client

class LoginWindow:
    def __init__(self, client):
        self.window = Tk()
        logging.info(f'-- AUTHENTICATION PROCESS... --')

        self.username = StringVar()
        self.password = StringVar()
        self.CLIENT = client

        Label(self.window, text='Username:').pack()
        Entry(self.window, textvariable=self.username).pack()
        Label(self.window, text='Password:').pack()
        Entry(self.window, textvariable=self.password, show='*').pack()
        Button(self.window, text='Login', command=self.loginValidation).pack()

        self.window.mainloop()

    def loginValidation(self):
        username = self.username.get()
        password = self.password.get()

        if self.CLIENT.login(username, password):
            messagebox.showinfo('Success', 'Logged in successfully!')
            logging.info(f'Username {username} and password {password}')
            self.CLIENT.send_msg('YESS')
            self.window.destroy()  # закрыть окно входа в систему
        else:
            messagebox.showerror('Error', 'Invalid username or password')


class Window:
    def __init__(self, client):
        self.window = Tk()

        self.text = StringVar()
        self.username = StringVar()
        self.CLIENT = client

        self.username.set('Plug')
        self.text.set('')
        self.window.title('CHAT')
        self.window.geometry('400x600')

        self.log = Text(self.window)
        self.nick = Entry(self.window, textvariable=self.username)
        self.msg = Entry(self.window, textvariable=self.text)

        self.msg.pack(side='bottom', fill='x', expand='true')
        self.nick.pack(side='bottom', fill='x', expand='true')
        self.log.pack(side='top', fill='both', expand='true')

    def startWindow(self):
        self.window.mainloop()




