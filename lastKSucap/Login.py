import tkinter as tk
import sqlite3
from tkinter import *
from tkinter.messagebox import showerror

class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry('800x800')
        self.window.resizable(False, False)

        bg = PhotoImage(file='pk.png')
        self.bg = tk.Label(self.window, width=800, height=800, image=bg)
        self.bg.pack()

        self.idEntry = tk.Entry(self.window, width=30)
        self.idEntry.place(relx=0.4, rely=0.402)

        self.passwordEntry = tk.Entry(self.window, width=30)
        self.passwordEntry.place(relx=0.4, rely=0.55)

        self.login = tk.Button(self.window, text="Login", command=self.login, width=14)
        self.login.place(relx=0.2, rely=0.67)

        self.buttonBack = tk.Button(self.window, text='Sign up', command=self.go_signup)
        self.buttonBack.place(relx=0.6, rely=0.67)


        self.window.mainloop()

    def go_signup(self):
        self.window.destroy()
        import Signup
        Signup.Signup()

    def go_student(self):
        id = self.idEntry.get()
        self.connection.close()
        self.window.destroy()
        import Student_Window
        Student_Window.Student_Window(id)

    def go_admin(self):
        self.connection.close()
        self.window.destroy()
        import Admin
        Admin.Admin()

    def login(self):
        if self.validation():
            self.connect_to_database()
            id = self.idEntry.get()
            password = self.passwordEntry.get()

            if self.check_account(id, password):
                curser = self.connection.execute(f"SELECT USER_TYPE FROM ACCOUNT WHERE ACCOUNT.ID = {id}")
                user_type = ""
                for x in curser:
                    user_type = x[0]
                if user_type == "student":
                    self.go_student()
                elif user_type == "admin":
                    self.go_admin()
            else:
                showerror(message="Invalid ID or Password")
        else:
            showerror(message=self.error_message)

    def validation(self):
        is_valid = True
        self.error_message = ""

        if len(self.idEntry.get()) != 10 or not self.idEntry.get().isdigit():
            is_valid = False
            self.error_message += "Invalid ID number"
        return is_valid

    def check_account(self, id, password):
        x = self.connection.execute("SELECT ID,PASSWORD FROM ACCOUNT")
        for y in x:
            if id == y[0] and password == y[1]:
                return True
        return False

    def connect_to_database(self):
        self.connection = sqlite3.connect("database.db")
