from tkinter import *
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from directory import atlas, colors
from Image_to_Text import Image_to_Text_AI
import textwrap



def inputWithGhostText(input, e, textbox=False):
    if not textbox:
        def onClick(event):
            e.delete(0, 'end')
            e.unbind('<Button-1>')

        e.insert(0, input)
        
        e.bind('<Button-1>', onClick)
    else:
        def onClick(event):
            e.delete("1.0", "end")
            e.unbind('<Button-1>')

        e.insert(textbox,input)
        e.bind('<Button-1>', onClick)

class Task:
    def __init__(self, root, name= False, description=False, due_date=False):
        self.isExists = True
        self.isDescriptionShow = False

        self.name = ""
        self.description = ""
        self.due_date = ""

        course_dic = atlas[2]
        self.parent_course = course_dic[root.winfo_parent()] # course object that task falls under

        self.root = Frame(root,bg=colors['center_color'], padx=50)

        self.left_frame = Frame(self.root, bg=colors['center_color'])
        self.right_frame = Frame(self.root, bg = "",padx=3)
        self.bottom_frame = Frame(self.root, bg = colors['center_color'],pady=5)
        
        
        self.task_name_frame = Frame(self.left_frame,bg=colors['center_color'], width=300, height=30)
        self.task_name = Label(self.task_name_frame, text=self.name, font='arial 14 bold', bg=colors['center_color'])
        self.task_name.bind('<Button-1>', self.clickName)
        
        
        self.task_description = Label(self.left_frame, text=self.description, bg=colors['center_color'], justify=LEFT, font='arial 12')
        self.task_description.bind('<Button-1>', self.clickDescription)
        
        
        self.task_due_date = Label(self.right_frame, text=self.due_date, padx=5, font='arial 10', bg=colors['center_color'])
        
        # initial entries
        self.name_entry = Entry(self.left_frame, width=25, font='Helvetica')
        
        self.description_text_box = Text(self.left_frame, height=5,width=25, wrap=WORD, font='Helvetica')

        self.date_string_variable = StringVar()
        self.due_date_label = Label(self.left_frame, text = "Due Date: ", bg='white')
        self.due_date_calendar = DateEntry(self.left_frame, selectmode='day', textvariable=self.date_string_variable)     

        self.enter_button = Button(self.bottom_frame, text="Enter", command=self.submit, bg=colors['center_color'])


        # load trash image
        #Open Image
        trash_open = Image.open('Icons/trash-9-48.png')
        #Resize Image
        trash_resized = trash_open.resize((15,15),Image.Resampling.LANCZOS)
        #Convert Image to PhotoImage
        self.trash_icon = ImageTk.PhotoImage(trash_resized)
        self.trash_button = Label(self.right_frame, bg=colors['center_color'],image=self.trash_icon) 
        self.trash_button.bind('<Button-1>', self.destroy)
        
        # load camera image
        camera_open = Image.open('Icons/camera.png')
        camera_resized = camera_open.resize((15,15),Image.Resampling.LANCZOS)
        self.camera_icon = ImageTk.PhotoImage(camera_resized)
        self.camera_button = Label(self.right_frame, bg=colors['center_color'], image=self.camera_icon)
        self.camera_button.bind('<Button-1>', self.deployAI)
        
        # grid main containers
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        

        self.root.grid()
        self.left_frame.grid(row=0, column=0, sticky="n")
        self.right_frame.grid(row=0, column=1,sticky='ne')
        self.bottom_frame.grid(row=1, column=0,columnspan=2,sticky='sw' )

        if not name and not description and not due_date:
            inputWithGhostText("Enter Name of Task",self.name_entry)
            self.name_entry.grid(columnspan=2, sticky='w')

            inputWithGhostText("Enter Description", self.description_text_box,textbox=INSERT)
            self.description_text_box.grid(columnspan=2, sticky='w')

            self.due_date_label.grid(sticky='w')
            self.due_date_calendar.grid(row=2,column=1, sticky='w')
            
            self.enter_button.grid(row=0, column=0, sticky='sw')

        else:
            self.name_entry.insert(0,name)
            self.description_text_box.insert(INSERT, description)
            self.date_string_variable.set(due_date)
            self.submit()
            
        self.trash_button.grid(row=0, column=2,sticky='ne')
        self.camera_button.grid(row=0, column=1, sticky='nw')

    def enterKeyPressedName(self, event):
        self.name_entry.grid_forget()
        self.name_entry.unbind('<Return>')
        self.name = self.name_entry.get()
        self.task_name.config(text='• '+self.name)
        self.task_name.grid(sticky='w')


    def enterKeyPressedDescription(self, event):
        self.description_text_box.grid_forget()
        self.description_text_box.unbind('<Return>')
        wrapper = textwrap.TextWrapper(width=25)
        self.description = wrapper.fill(text=self.description_text_box.get("1.0",'end-1c'))
        self.task_description.config(text=self.description)
        self.task_description.grid()
        
    def submit(self):
        self.task_name_frame.grid_propagate(0)

        wrapper = textwrap.TextWrapper(width=25)

        self.name = self.name_entry.get()
        self.description = wrapper.fill(text=self.description_text_box.get("1.0",'end-1c'))
        self.due_date = self.date_string_variable.get()

        self.task_name.config(text='• '+self.name)
        self.task_description.config(text=self.description)
        self.task_due_date.config(text='Due ' +self.due_date)

        self.task_name.grid()        
        self.task_name_frame.grid(sticky='w')
        self.task_due_date.grid(row=0, column=0, sticky='e')

        tl = atlas[0]

        # if called by add task button
        if self.name_entry.winfo_ismapped():

            self.name_entry.grid_forget()
            self.description_text_box.grid_forget()
            self.due_date_label.grid_forget()
            self.enter_button.grid_forget()
            self.due_date_calendar.grid_forget()
            tl.update()
        
        else:
            self.hide()
       

    def changeName(self):
        self.name_entry.grid(sticky='w')
        self.name_entry.bind('<Return>', self.enterKeyPressedName)
      
    def changeDescription(self):
        self.description_text_box.grid(sticky='w')
        self.description_text_box.bind('<Return>', self.enterKeyPressedDescription)

    def clickName(self, event):
        if self.isDescriptionShow:
            self.task_description.grid_forget()
            self.isDescriptionShow = False
        else:
            self.task_description.grid(sticky='w')
            self.isDescriptionShow = True

    def clickDescription(self, event):
        self.changeDescription()
      
    def display(self):
        self.root.grid()

    def hide(self):
        self.root.grid_forget()

    def destroy(self, event):
        self.root.destroy()
        self.isExists = False

        tl = atlas[0]
        tl.update()
    
    def deployAI(self, event):
        ai = Image_to_Text_AI()
        text = ai.imageToText()
        self.description_text_box.delete("1.0", "end")
        self.description_text_box.unbind('<Button-1>')
        self.description_text_box.insert(INSERT, text)
    
if __name__ == '__main__':
    ws = Tk()
    t =Task(ws)
    ws.mainloop()

    