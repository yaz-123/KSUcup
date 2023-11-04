import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
import sqlite3
import re

class Signup:
    def __init__(self):
        self.window = tk.Tk()
        self.connect_to_database()
        self.create_table()
        self.create_admin()
        self.setbooked()
        #self.create_booking()

        bg =PhotoImage(file='pk.png')

        self.window.title("Sign up")
        self.window.geometry('800x800')
        self.window.geometry("+600+200") # to position the window in the center
        self.window.resizable(False, False)

        self.bg = tk.Label(self.window, width=800, height=800, image=bg)
        self.bg.pack()

        self.first_name = tk.Entry(self.window, width=35)
        self.first_name.place(relx=0.39, rely=0.27)

        self.last_name = tk.Entry(self.window, width=35)
        self.last_name.place(relx=0.39, rely=0.325)

        self.student_id = tk.Entry(self.window, width=35)
        self.student_id.place(relx=0.39, rely=0.382)

        self.password = tk.Entry(self.window, width=35)
        self.password.place(relx=0.39, rely=0.44)

        self.email = tk.Entry(self.window, width=35)
        self.email.place(relx=0.39, rely=0.496)

        self.phone_number = tk.Entry(self.window, width=35)
        self.phone_number.place(relx=0.39, rely=0.553)

        self.submit = tk.Button(self.window, text="Submit", command=self.submit, width=14)
        self.submit.place(relx=0.39, rely=0.63)

        self.buttonBack = tk.Button(self.window, text='Login', command=self.go_Login)
        self.buttonBack.place(relx=0.61, rely=0.63)

        self.create_admin()
        self.window.mainloop()

    def go_Login(self):
        self.connection.close()
        self.window.destroy()
        import Login
        Login.Login()

    def connect_to_database(self):
        self.connection = sqlite3.connect("database.db")
        #self.display_data()

    def validation(self):
        is_valid = True
        self.error_message = ""

        if self.first_name.get().strip() == "" or not self.first_name.get().isalpha() or self.first_name.get().isspace(): #and #not self.first_name.get().isdigit():
            is_valid = False
            self.error_message += "Invalid First name\n"

        elif self.last_name.get().strip() == "" or not self.last_name.get().isalpha() or self.last_name.get().isspace():
            is_valid = False
            self.error_message += "Invalid Last name\n"

        elif not self.student_id.get().isdigit() or not len(self.student_id.get())  == 10 or self.student_id.get().isspace():
            is_valid = False
            self.error_message += "Invalid ID number\n"

        elif len(self.password.get()) < 6  or not self.password.get().isalnum() or self.password.get().isspace():# or not ((type(self.password.get()) == str) or (type(self.password.get()) == int)) :
            is_valid = False
            self.error_message += "Invalid Password\n"

        elif not self.check_email(): #and not self.check_email(self.email.get()):
            is_valid = False
            self.error_message += "Invalid Email address\n"

        elif not self.phone_number.get().startswith("05") or not self.phone_number.get().isnumeric() or len(self.phone_number.get()) != 10  or self.phone_number.get().isspace():
            is_valid = False
            self.error_message += "Invalid phone number\n"
        return is_valid

    def submit(self):
        if self.validation():
            f_name = self.first_name.get()
            l_name = self.last_name.get()
            id = self.student_id.get()
            password = self.password.get()
            email = self.email.get()
            phone = self.phone_number.get()
            user_type = "student"

            try:
                self.connection.execute(f'''INSERT INTO ACCOUNT (ID,FIRST_NAME,LAST_NAME,PASSWORD,EMAIL,PHONE,USER_TYPE) VALUES ('{id}','{f_name}','{l_name}','{password}','{email}','{phone}','{user_type}');''')
                self.connection.commit()

                self.first_name.delete(0,"end")
                self.last_name.delete(0,"end")
                self.student_id.delete(0,"end")
                self.password.delete(0,"end")
                self.email.delete(0,"end")
                self.phone_number.delete(0,"end")

                showinfo(message = "Account created successfully")
            except sqlite3.IntegrityError:
                showerror(message = "Account already exist")
        else:
            showerror(message=self.error_message)

    def create_table(self):
        try:
            self.connection.execute('''CREATE TABLE ACCOUNT
                   (
                    ID              VARCHAR(10)     PRIMARY KEY     NOT NULL,
                    FIRST_NAME      TEXT                            NOT NULL,
                    LAST_NAME       TEXT                            NOT NULL,
                    PASSWORD        TEXT                            NOT NULL,
                    EMAIL           VARCHAR(20)                     NOT NULL,
                    PHONE           VARCHAR(10)                     NOT NULL,
                    USER_TYPE       VARCHAR(10)                     NOT NULL
                    );''')
            self.connection.commit()
            print("")
        except sqlite3.OperationalError:
            print("")
        try:
            self.connection.execute('''CREATE TABLE EVENT
                 (
                  NAME            TEXT                            NOT NULL,
                  LOCATION        TEXT                            NOT NULL,
                  CAPACITY        VARCHAR(20)                     NOT NULL,
                  DATE            DATETIME                        NOT NULL,
                  NUMBER          VARCHAR(5)     PRIMARY KEY      NOT NULL,
                  BOOKED          VARCHAR(20)                     NULL
                  );''')
            self.connection.commit()
        except sqlite3.OperationalError:
            print("")
        try:
            self.connection.execute('''CREATE TABLE BOOKING
                 (
                  NUMBER          VARCHAR(5)                      NOT NULL,
                  ID              VARCHAR(10)                     NOT NULL
                  );''')
            self.connection.commit()
        except sqlite3.OperationalError:
            print("")

    def create_admin(self):
        try:
            self.connection.execute(f'''INSERT INTO ACCOUNT (ID,FIRST_NAME,LAST_NAME,PASSWORD,EMAIL,PHONE,USER_TYPE) VALUES \
            ('1234567891','admin','admin','123456','admin@ksu.edu.sa','0512345678','admin'); ''')
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("")

    #def create_booking(self):
        #try:
            #self.connection.execute(f'''INSERT INTO BOOKING (ID,NUMBER) VALUES ('1234567891','10000');''')
            #self.connection.commit()
        #except sqlite3.IntegrityError:
            #print("")

    def setbooked(self):
        self.connection.execute('''UPDATE EVENT SET BOOKED=0 WHERE BOOKED IS NULL;''')
        self.connection.commit()

    def check_email(self):
        e=self.email.get()
        regex ="^([A-z0-9\._-]+)@(ksu).(edu).(sa)$"
        if re.search(regex, e):
            return True
        else:
            return False

    def display_data(self):
        data = self.connection.cursor()
        for row in data.execute('SELECT * FROM ACCOUNT;'):
            print(row)


Signup()