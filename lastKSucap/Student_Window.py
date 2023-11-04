import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from tkinter import *
import sqlite3
import logging
from tkinter import ttk




class Student_Window:
    def __init__(self, id):
        self.window = tk.Tk()
        self.window.title("Student Window")
        self.window.geometry('800x800')
        self.window.resizable(False, False)
        self.connect_to_database()

        self.id =id

        #bg = PhotoImage(file='pk.png')
        #self.bg = tk.Label(self.window, width=800, height=800, image=bg)
        #self.bg.pack()


        #logging.basicConfig(filename="transaction.log", filemode="a",format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'", level=logging.INFO)

        taps = ttk.Notebook(self.window)
        tap1 = ttk.Frame(taps)
        tap2 = ttk.Frame(taps)
        taps.add(tap1,text='Book a Ticket')
        taps.add(tap2,text='View my tickets')
        taps.pack(expand=1, fill="both")

        self.buttonlogout = tk.Button(tap1, text='Logout', command=self.logout)
        self.buttonlogout.place(relx=0.39, rely=0.63)

        self.button2logout = tk.Button(tap2, text='Logout', command=self.logout)
        self.button2logout.place(relx=0.39, rely=0.63)

        self.buttonbook = tk.Button(tap1, text='Book', command=self.book)
        self.buttonbook.place(relx=0.39, rely=0.80)

        self.buttonshow = tk.Button(tap2, text='Show', command=self.showdata)
        self.buttonshow.place(relx=0.39, rely=0.80)

        self.tv = ttk.Treeview(tap1, columns=(1, 2, 3, 4), show='headings', height=8,selectmode=tk.BROWSE)
        self.tv.heading(1, text="ID")
        self.tv.heading(2, text="EVENT NAME")
        self.tv.heading(3, text="LOCATION")
        self.tv.heading(4, text="DATE AND TIME")
        self.tv.place(relx=0.0, rely=0.0)
        self.tv.pack
        self.diplaydata()

        self.tv2 = ttk.Treeview(tap2, columns=(1, 2, 3), show='headings', height=8, selectmode=tk.BROWSE)
        self.tv2.heading(1, text="EVENT NAME")
        self.tv2.heading(2, text="LOCATION")
        self.tv2.heading(3, text="DATE AND TIME")
        self.tv2.place(relx=0.0, rely=0.0)
        self.tv2.pack




        self.window.mainloop()

    def logout(self):
        self.connection.close()
        self.window.destroy()
        import Signup
        Signup.Signup()

    def book(self):
        selected = self.tv.focus()
        details = self.tv.item(selected)
        try:
            idnumber = details.get("values")[0]
            if self.bookvalidation(idnumber):
                try:
                    self.connection.execute(f'''INSERT INTO BOOKING (ID,NUMBER) VALUES ('{self.id}','{idnumber}');''')
                    self.connection.commit()
                    self.connection.execute('''UPDATE EVENT SET BOOKED = BOOKED + 1;''')
                    self.connection.commit()
                    print("inserted")
                except sqlite3.OperationalError:
                    print("")
            else:
                print("can not insert")
        except:
            print("nothing selected")

    def bookvalidation(self, num):
        c = self.connection.execute(f"SELECT CAPACITY FROM EVENT WHERE {num} == NUMBER")
        b = self.connection.execute(f"SELECT BOOKED FROM EVENT WHERE {num} == NUMBER")

        if c.fetchone() > b.fetchone():
            if self.get_numbers(num):
                print("all good")
                return True
            else:
                print("this id been booked this event before")
                return False
        else:
            print('full')
            return False

    def get_numbers(self, num):
        cursor = self.connection.execute(f"SELECT NUMBER,ID FROM BOOKING WHERE ID = {self.id}")
        l = [1]
        for x in cursor:
            l.append(x[0])
        for y in l:
            #print(str(y) + ' this y')
            #print(str(num) + ' this num')
            #print(y == num)
            if int(y) == int(num):
                print("THERE IS DUPLICATE")
                return False
        print("NO DUPLICATE")
        return True

    #def showdata(self):
        #cur = self.connection.execute(f"SELECT NUMBER FROM BOOKING WHERE {self.id} == ID")
        #l = []
        #print(cur.fetchall())
        #print(cur.fetchall())
        #bur = self.connection.execute(f"SELECT NAME, LOCATION, DATE FROM EVENT WHERE EVENT.NUMBER == {cur.fetchall()}")
        #print(bur.fetchall())
        #for x in cur.fetchall():
            #l.append(x)
            #print(x)
        #print(l)
        #j1 = self.connection.execute(f"SELECT NAME, LOCATION, DATE FROM EVENT WHERE {l} == NUMBER")
        #count = 0
        #for row in j1:
            #print(row)
        #for row in j1:
            #self.tv2.insert(parent='', index=count, text='', values=(row[0], row[1], row[2]))
            #count += 1

    def showdata(self):
        cur = self.connection.execute(f"SELECT EVENT.NAME, EVENT.LOCATION, EVENT.DATE, EVENT.NUMBER FROM EVENT, BOOKING WHERE {self.id} == BOOKING.ID AND BOOKING.NUMBER == EVENT.NUMBER")
        count = 0
        l = []
        for row in cur:
            print(row[3])
            print(l)
            if str(row[3]) in l:
                print('not again')
            else:
                self.tv2.insert(parent='', index=count, text='', values=(row[0], row[1], row[2]))
                count += 1
                l.append(row[3])
                print('you are good')



    #def log_writer(self, sender, amount, receiver):
        #logging.info(f"Amount: {amount}, Sender wallet number: {sender}, Receiver wallet number: {receiver}")

    def diplaydata(self):
        cur = self.connection.execute("SELECT NUMBER, NAME, LOCATION, DATE from EVENT")
        count = 0
        for row in cur:
            self.tv.insert(parent='', index=count, text='', values=(row[0], row[1], row[2], row[3]))
            count += 1

    def connect_to_database(self):
        self.connection = sqlite3.connect("database.db")
