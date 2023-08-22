from tkinter import *
from tkinter import ttk
import Task
from directory import atlas, colors


class Course:

    def __init__(self, name, period, root, frame, color, icon, tag):
        self.name = name
        self.period = period
        self.root = root
        self.color = color
        self.frame = frame
        self.icon = icon
        self.tag = tag 

        self.tasks = []

        self.isShow = False
        self.isEditMode = False
        
        self.bigger_frame = Frame(self.frame, bg=colors['center_color'])
        self.personal_frame = Frame(self.bigger_frame, pady=10, bg=colors['center_color'])    
        self.add_task_button = Button(self.personal_frame, text="Add Task", command=self.addTask, bg=colors['top_buttons_color'])
        self.course_button = Button(self.personal_frame, text="  "+self.period+". " + self.name+ "  ",  fg=self.color, command=self.showTask, font="arial 16", bg=colors['top_buttons_color'], image=self.icon, compound=LEFT)
        self.separator = ttk.Separator(self.bigger_frame, orient='horizontal')

        self.course_dic = atlas[2]
        self.course_dic[str(self.bigger_frame)] = self


        # Edit Mode 
        self.add_course_frame = Frame(self.bigger_frame, padx=10, bg=colors['center_color'])
        self.course_name_entry = Entry(self.add_course_frame)
        self.course_name_entry.insert(0, self.name)
        self.course_period_entry = Entry(self.add_course_frame)
        self.course_period_entry.insert(0, self.period)
        self.course_color_entry = Entry(self.add_course_frame)
        self.course_color_entry.insert(0, self.color)
        self.enter_button = Button(self.add_course_frame, text="Enter", command=self.edit, bg=colors['top_buttons_color'])
        self.delete_button = Button(self.add_course_frame, text="DELETE", bg='red', fg='white', command=self.delete)

    def display(self):
        self.course_button.grid(row=0, sticky='w') 
        self.personal_frame.grid(sticky='w')
        self.bigger_frame.grid(row=self.period, sticky='w')
        self.separator.grid(sticky='ew', ipadx=300)

     
    def showTask(self):
            
            if not self.isShow:
                self.add_task_button.grid(sticky='w')
                for task in self.tasks:
                    if(task.isExists):
                      task.display()
                    else:
                      self.tasks.remove(task)
                      del task
                self.isShow = True
                
            else:
                self.add_task_button.grid_forget()
                for task in self.tasks:
                    if(task.isExists):
                      task.hide()
                    else:
                      self.tasks.remove(task)
                      del task
                self.isShow = False


    def addTask(self, n=False, d=False, dd=False):
        if not n and not d and not dd:
          newTask = Task.Task(self.personal_frame)
          self.tasks.append(newTask)
        else:
          newTask = Task.Task(self.personal_frame, name=n, description=d, due_date=dd)
          self.tasks.append(newTask)
          tl = atlas[0]
          tl.update()
        
        

    def edit(self, custom=False, period=0):
        
        # peak brain function i am awesome

        self.bigger_frame.grid_forget()
        if not custom:
          temp = self.period
          self.period = self.course_period_entry.get()
          self.name = self.course_name_entry.get()
          self.color = self.course_color_entry.get()
          self.course_button.config(text="  "+self.period+". " + self.name + "  ", fg=self.color)
          tl = atlas[0]
          tl.update()
          if not self.frame.grid_slaves(row=self.period):
            self.display()

          else:
            course_in_period = self.course_dic[str(self.frame.grid_slaves(row=self.period)[0])]
            course_in_period.edit(custom=True, period=temp)
            self.display()

        else:

          self.period = period
          self.course_button.config(text="  "+self.period+". " + self.name+"  ")
          self.course_period_entry.delete(0,END)
          self.course_period_entry.insert(0, self.period)
          self.display()


    def toggleEditMode(self):
        
        if not self.isEditMode:
            self.delete_button.grid(row=0, column=1)
            self.course_name_entry.grid()     
            self.course_period_entry.grid()
            self.course_color_entry.grid()
            self.enter_button.grid(sticky='w')
            self.add_course_frame.grid(row=0,column=1,sticky='e')
            
            self.isEditMode = True

        else:
            self.add_course_frame.grid_forget()
            self.isEditMode = False

    def delete(self):
        for task in self.tasks:
            task.destroy('event')

        self.showTask()
        course_list = atlas[1]
        course_list.remove(self)
        self.bigger_frame.grid_forget()
        self.bigger_frame.destroy()
        del self

if __name__ == '__main__':
  import os
  from PIL import ImageTk, Image
  root = Tk()

  # config the root window
  root.geometry('300x200')
  root.resizable(False, False)
  root.title('Combobox Widget')
  icons_list = []
  
  # populating icons_list with all images in selectable_icons
  d = 'Selectable_Icons'
  for filename in os.listdir(d):
      f = os.path.join(d, filename)
      if os.path.isfile(f):
          icons_list.append(f)
  selected_icon_int = IntVar()
  images = []
  for count, icon in enumerate(icons_list):
  
            icon_open = Image.open(icon)
            #Resize Image
            icon_resized = icon_open.resize((15,15),Image.ANTIALIAS)
            #Convert Image to PhotoImage
            img = ImageTk.PhotoImage(icon_resized) 
            images.append(img)
            img_button = Radiobutton(root, variable=selected_icon_int, value=count, image=img) 

  
            img_button.grid()


  root.mainloop()
  
    
        
        
        
        



  