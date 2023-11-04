import tkinter as tk
import datetime
import random
from tkinter import *
import sqlite3
import csv
from tkinter.messagebox import showerror, showinfo

class Admin:
   def __init__(self):
      self.window = tk.Tk()
      self.window.title("Admin")
      self.window.geometry('800x800')
      self.window.resizable(False, False)
      self.connect_to_database()

      bg = PhotoImage(file='pk.png')
      self.bg = tk.Label(self.window, width=800, height=800, image=bg)
      self.bg.pack()

      self.event_name = tk.Entry(self.window, width=35)
      self.event_name.place(relx=0.39, rely=0.27)

      self.event_location = tk.Entry(self.window, width=35)
      self.event_location.place(relx=0.39, rely=0.325)

      self.event_capacity = tk.Entry(self.window, width=35)
      self.event_capacity.place(relx=0.39, rely=0.382)

      self.date = tk.Entry(self.window, width=35)
      self.date.place(relx=0.39, rely=0.44)


      self.Create = tk.Button(self.window, text='Create', command=self.create)
      self.Create.place(relx=0.49, rely=0.63)

      self.Backup = tk.Button(self.window, text='Backup', command=self.backup)
      self.Backup.place(relx=0.59, rely=0.63)

      self.buttonBack = tk.Button(self.window, text='Logout', command=self.logout)
      self.buttonBack.place(relx=0.39, rely=0.63)


      self.window.mainloop()

   def logout(self):
      self.connection.close()
      self.window.destroy()
      import Signup
      Signup.Signup()

   def backup(self):
      file = open("backup.csv", 'a', newline="")
      data = csv.writer(file)

      f = ["____________"]
      data.writerow(f)

      t = [f"Time {self.time_date()}"]
      data.writerow(t)

      for table in ["ACCOUNT", "EVENT", "BOOKING"]:
         data.writerow([f"{table} table"])
         m = self.connection.execute(f"SELECT * FROM {table}")
         for x in m:
            data.writerow(x)
      file.close()
      showinfo(message="Backup created")

   def time_date(self):
      time = datetime.datetime.now()
      time = time.strftime("%H:%M:%S--%d/%m/%Y")
      return time

   def validation(self):
      is_valid = True
      self.error_message = ""

      if self.event_name.get().strip() == "" or not self.event_name.get().isalpha():
         is_valid = False
         self.error_message += "Invalid event name\n"

      elif self.event_location.get().strip() == "" or not self.event_location.get().isalpha():
         is_valid = False
         self.error_message += "Invalid event location\n"

      elif self.event_capacity.get().strip() == "" or not self.event_capacity.get().isdigit() or self.event_capacity.get().isspace():
         is_valid = False
         self.error_message += "Invalid event capacity\n"

      elif self.cheak_date_time()==False:
         is_valid = False
         self.error_message += "Invalid date or time\n"
      return is_valid


   def create(self):
      if self.validation():
         e_name = self.event_name.get()
         e_location = self.event_location.get()
         capacity = self.event_capacity.get()
         date = self.date.get()
         e_number = self.generate_booking_number()


         self.connection.execute(
            f'''INSERT INTO EVENT (NAME,LOCATION,CAPACITY,DATE,NUMBER) VALUES ('{e_name}','{e_location}','{capacity}','{date}','{e_number}');''')
         self.connection.commit()

         self.event_name.delete(0, "end")
         self.event_location.delete(0, "end")
         self.event_capacity.delete(0, "end")
         self.date.delete(0, "end")
         self.connection.execute('''UPDATE EVENT SET BOOKED=0 WHERE BOOKED IS NULL;''')
         self.connection.commit()

         showinfo(message="Event been created")
      else:
         showerror(message=self.error_message)


   def check_booking_number(self, booking_number):
      x = self.connection.execute(f"SELECT NUMBER FROM EVENT")
      for y in x:
         if booking_number == y[0]:
            return False
      return True

   def generate_booking_number(self):
      booking_number = random.randint(10000,50000)
      while not self.check_booking_number(booking_number):
         booking_number = random.randint(10000, 50000)
      return booking_number

   def connect_to_database(self):
      self.connection = sqlite3.connect("database.db")



   def cheak_date_time(self):
      try:
         dateg = datetime.datetime.strptime(self.date.get(), '%Y/%m/%d/%H/%M')
         if dateg > datetime.datetime.now():
            return True
         else:
            return False
      except ValueError:
         return False



