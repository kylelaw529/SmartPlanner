from tkinter import *
from datetime import datetime, timedelta
from threading import Thread
import time
from Send_Text_Message import send_message
from directory import colors

class Settings(Frame):
    
    def __init__(self, root, name, top_frame):

        Frame.__init__(self, root)

        self.width = 500
        self.height = 500
        self.root = root
        self.name = name
        self.phone_number = '5164620537'
        self.title_label = top_frame

        self.current_time = datetime.strptime(datetime.now().strftime("%H:%M %p"), "%H:%M %p")

        try:    # if there is a valid time in storage preference then use that else set to 3:00 PM
            with open('Storage/Settings_Preferences_Storage.txt', 'r') as file:
                self.homework_time_string = file.readlines()[0].strip()
                self.homework_time = datetime.strptime(datetime.strptime(self.homework_time_string, '%I:%M %p').strftime('%H:%M'),"%H:%M")

        except:
            self.homework_time_string = "3:00 PM"
            self.homework_time = datetime.strptime(datetime.strptime(self.homework_time_string, '%I:%M %p').strftime('%H:%M'),"%H:%M")

        self.time_remaining = self.homework_time-self.current_time

        self.config(bg=colors['top_buttons_color'], width=self.width, height=self.height, highlightbackground='black', highlightthickness=3)

        self.grid_propagate(0)

        self.top_frame = Frame(self, bg = colors['top_color'], height=self.height*0.1)
        self.center_frame = Frame(self, bg=colors['top_buttons_color'],height=self.height*0.7, padx=5, pady=10)
        self.bottom_frame = Frame(self, bg=colors['top_buttons_color'],height=self.height*0.2)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=2)

        # populating TOP FRAME
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.settings_label = Label(self.top_frame, text = "Settings", bg=colors['top_color'], font=('Comic Sans MS',20), fg='white')
        self.settings_label.grid(column=1, row=0,sticky='w')

        # populating CENTER FRAME
        self.center_frame.grid_columnconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.homework_time_label = Label(self.center_frame, text="Set Homework Time (H:MM PM/AM):    " + self.homework_time_string, bg=colors['top_buttons_color'])
        self.homework_time_entry = Entry(self.center_frame, bg='white')
        self.homework_time_entry.bind('<Return>', self.homeworkTimeEnter)
        self.homework_time_label.grid(row=0, column=0, sticky='w')
        self.homework_time_entry.grid(row=0, column=1, sticky='e')

        
        self.change_name_label = Label(self.center_frame, text='Name: ', bg=colors['top_buttons_color'])
        self.change_name_entry = Entry(self.center_frame, bg='white')
        self.change_name_entry.bind('<Return>', self.changeNameEnter)
        self.change_name_label.grid(row=1, column=0, sticky='w', pady=10)
        self.change_name_entry.grid(row=1, column=1, sticky='e',pady=10)


        self.phone_number_label = Label(self.center_frame,text='Phone Number: ' + self.phone_number, bg=colors['top_buttons_color'])
        self.phone_number_entry = Entry(self.center_frame, bg='white')
        self.phone_number_entry.bind('<Return>', self.phoneNumberEnter)
        self.phone_number_label.grid(row=2, column=0, sticky='w')
        self.phone_number_entry.grid(row=2, column=1, sticky='e')
    

        # populating BOTTOM FRAME
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        self.close_button = Button(self.bottom_frame, text="Close", command=self.lower, width=12, height=1)
        self.close_button.grid(row=1, column=0, sticky='sw', padx=10, pady=10)



        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.center_frame.grid(row=1, column=0, sticky='nsew')
        self.bottom_frame.grid(row=2, column=0, sticky='nsew')

        self.run = True

        self.countdown()
        
    def countdown_worker(self):
        self.current_time = datetime.strptime(datetime.now().strftime("%H:%M %p"), "%H:%M %p")
        while self.run:
            if self.time_remaining == timedelta(days=0, minutes=0, seconds=0):
                break
            else:
                self.current_time = datetime.strptime(datetime.now().strftime("%H:%M %p"), "%H:%M %p")
                self.time_remaining = self.homework_time-self.current_time
                time.sleep(1)


       

    def homeworkTimeEnter(self, event):

        self.homework_time_string = self.homework_time_entry.get()
        self.homework_time = datetime.strptime(datetime.strptime(self.homework_time_string, '%I:%M %p').strftime('%H:%M'),"%H:%M")
        self.homework_time_label.config(text="Set Homework Time (H:MM PM/AM):    " + self.homework_time_string)
        self.homework_time_entry.delete(0,'end')

        

    def schedule_check(self, t):
        """
        Schedule the execution of the `check_if_done()` function after
        one second.
        """
        self.root.after(1000, self.check_if_homework_time, t)

    def check_if_homework_time(self, t):

        if not t.is_alive():
            # send text message
            message = "HEY! It's time to do homework!"
            send_message(message, self.phone_number)

            # after 60 seconds, restart the countdown --------- not done
      
            print("done")
        else:
            # Otherwise check again after one second.
            self.schedule_check(t)

    def countdown(self):
        countdown_thread = Thread(target=self.countdown_worker)
        countdown_thread.start()
        self.schedule_check(countdown_thread)
    
    def changeNameEnter(self, event):
        self.name = self.change_name_entry.get()
        self.title_label.config(text=self.name+"'s SmartPlanner")
        self.change_name_entry.delete(0, 'end')

    def phoneNumberEnter(self,event):
        self.phone_number = self.phone_number_entry.get()
        self.phone_number_label.config(text='Phone Number: ' + self.phone_number)
        self.phone_number_entry.delete(0,'end')

if __name__ == '__main__':
    root = Tk()
    window = Settings(root=root)
    root.grid()
    window.grid()
    window.countdown()
    root.mainloop()