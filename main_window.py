from tkinter import *
from Calendar_Agenda import Agenda
from Course import Course
import Task
from Task_List import Task_List
import directory
import os
from PIL import ImageTk, Image
import pickle
from Settings_Window import Settings


# creates frame which prompts user for course name and period
def addCourse():

    #creates course object using user input for name and period number, 
    def createCourse():
        new_name = course_name_entry.get()
        new_period = course_period_entry.get()

        global colors_index 
        if colors_index< len(colors)-1:
          color = colors[colors_index]

        else:
          colors_index=0
          color = colors[colors_index]
        colors_index+=1

        global course_tag
        new_course = Course(new_name, new_period, left_frame, courses_frame, color, icons_dict[selected_icon_int.get()], course_tag)
        course_tag+=1

        new_course.display()
        course_list.append(new_course)
        add_course_frame.grid_forget()
    
    
    
    def populateIconSelector():
        
        int_vars.append(selected_icon_int)
        icon_column = 0
        icon_row = 0
        for count, icon in enumerate(icons_list):
          
            icon_open = Image.open(icon)
            #Resize Image
            icon_resized = icon_open.resize((30,30),Image.Resampling.LANCZOS)
            #Convert Image to PhotoImage
            img = ImageTk.PhotoImage(icon_resized) 
            
            images.append(img)
            img_button = Radiobutton(icons_select_frame, variable=selected_icon_int, value=count, image=img, bg=center_color) 

            
            img_button.grid(column=icon_column, row=icon_row)
            icon_row+=1
            if (count+1)%3==0:
                icon_row=0
                icon_column+=1
            
            

    add_course_frame = Frame(courses_frame, bg=center_color)
    course_name_entry = Entry(add_course_frame, font="arial 16")
    course_period_entry = Entry(add_course_frame, font="arial 16")
    pick_icon_label = Label(add_course_frame, bg=center_color, font="arial 16", text="Choose an Icon: ")
    icons_select_frame = Frame(add_course_frame)
    
    
    selected_icon_int = IntVar(icons_select_frame, 0) 

    populateIconSelector()

    Task.inputWithGhostText("Enter Course Name", course_name_entry)
    course_name_entry.grid()
    Task.inputWithGhostText("Enter Course Period", course_period_entry)
    course_period_entry.grid()

    enter_button = Button(add_course_frame, text="Enter",command=createCourse, font="arial 16", bg=top_buttons_color)
    pick_icon_label.grid(sticky='w')
    icons_select_frame.grid(sticky='w')
    enter_button.grid(row=4,column=0,sticky='w')
    add_course_frame.grid(sticky='w')
    editCourses()



def editCourses():
    global edit_mode
    for course in course_list:
        course.toggleEditMode()

    if not edit_mode:
        add_new_course.grid(pady=10)
        edit_mode = True
    else:
        add_new_course.grid_forget()
        edit_mode = False


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as data_file:
        return pickle.load(data_file)


def show_calendar():
    for frame in root.grid_slaves():
        frame.grid_forget()
    agenda.update()
    agenda.display_events()
    agenda.grid(row=0, rowspan=2, column=0, sticky='nsew')
    btm_frame.grid(row=2, column=0, sticky='nsew')

def show_planner():
    for frame in root.grid_slaves():
        frame.grid_forget()
    settings_frame.grid(row=1, column=0)
    settings_frame.lower()
    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=2, sticky="ew")






# unique tag given to courses when created or loaded which allows course objects to be referenced to load tasks
course_tag = 0

# list of all created Course objects
course_list = []

# saving data then initializing courses with this data when run
course_data = []

# dictionary that references course object by path name of bigger_frame
course_dic = {}

colors = ["red", "orange", "green", "blue", "violet","black","beige","gold", "coral" ]
colors_index = 0

try:
    with open('Storage/Settings_Preferences_Storage.txt', 'r') as file:
            profile_name = file.readlines()[1]
            displayText = profile_name+"'s "
except:
    profile_name = ""

# list used to anchor image object and tkinter intVariable (necessary for it to work even thought they are never accessed)
images = []
int_vars = []

icons_list = []
icons_dict = {}
# populating icons_list with all images in selectable_icons
d = 'Selectable_Icons'
for filename in os.listdir(d):
    f = os.path.join(d, filename)
    if os.path.isfile(f):
        icons_list.append(f)

edit_mode = False



root = Tk()
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry("%dx%d" % (width/2, height/2))
root.state('zoomed')
root.wm_title( 'SmartPlanner')


for count, icon in enumerate(icons_list):
    icon_open = Image.open(icon)
    #Resize Image
    icon_resized = icon_open.resize((30,30),Image.Resampling.LANCZOS)
    #Convert Image to PhotoImage
    img = ImageTk.PhotoImage(icon_resized) 
    icons_dict[count] = img

top_color ='#54BAB9'
center_color = '#E9DAC1' 
top_buttons_color = '#EAE3D2'

directory.add_to_colors('top_color','#54BAB9')
directory.add_to_colors('center_color', '#E9DAC1')
directory.add_to_colors('top_buttons_color', '#EAE3D2')
    

# main containers
top_frame = Frame(root, bg=top_color, width=450, height=500, pady=20, padx=20)
center = Frame(root, bg=center_color, width=50, height=40, padx=3, pady=3, highlightbackground="white", highlightthickness=3)
btm_frame = Frame(root, bg='grey', width=450, height=45, pady=3)
right_frame = Frame(center, bg= center_color,padx=3, pady=3, width=50,)
left_frame = Frame(center, bg= center_color, padx=3, pady=3, width=50)



# layout main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
center.grid_rowconfigure(1, weight=1)
center.grid_columnconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)
center.grid_columnconfigure(2, weight=1)
top_frame.grid_rowconfigure(1, weight=1)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)
btm_frame.grid_columnconfigure(0, weight=1)
btm_frame.grid_columnconfigure(1, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=2, sticky="ew")


# populating CENTER FRAME
right_frame.grid(column=1, row=0, sticky='n',padx=50, columnspan=2)
left_frame.grid(column=0, row=0, sticky='ns', padx=50)

courses_label = Label(left_frame, text='Courses', font='Helvetica 20 underline', bg= center_color)
courses_label.grid()

courses_frame = Frame(left_frame, bg=center_color)
courses_frame.grid(row=1,column=0, sticky='w')

add_new_course = Button(left_frame, text="Add New Course", command=addCourse, bg= top_buttons_color, width=25, height=2, font='arial 16')

# populating TOP FRAME
edit_button = Button(top_frame, text= 'Edit', bg=top_buttons_color, command=editCourses, width=12, height=1, font='Helvetica 15')
edit_button.grid(column=0, row=0, sticky='w')

title_label = Label(top_frame, text=displayText + 'SmartPlanner', bg=top_color , height=1, font=('Comic Sans MS',30), fg='white')
title_label.grid(column=1, row=0)

settings_frame = Settings(root=root, name=profile_name, top_frame=title_label)
settings_frame.grid(row=1, column=0)
settings_frame.lower()

settings_button = Button(top_frame, text='Settings', bg=top_buttons_color, command=settings_frame.lift, width=12, height=1, font='Helvetica 15')
settings_button.grid(column=2, row=0, sticky='e')




# populating RIGHT FRAME
tl = Task_List(right_frame)
tl.display()

upcoming_tasks_label = Label(right_frame, text='Upcoming Tasks', font='Helvetica 20 underline', bg= center_color)
upcoming_tasks_label.grid()


# populating BOTTOM FRAME
calendar_button = Button(btm_frame, text="Calendar", bg=top_buttons_color, font="Helvetica 15", command=show_calendar)
planner_button = Button(btm_frame, text="Planner", bg=top_buttons_color, font="Helvetica 15", command=show_planner)

agenda = Agenda(tl, master=root, selectmode='none')

calendar_button.grid(row=0, column=1)
planner_button.grid(row=0, column=0)

# add objects to directory atlas so they can be referenced in other modules
directory.add_to_atlas(tl)
directory.add_to_atlas(course_list)
directory.add_to_atlas(course_dic)

# Load in saved data 
load_course_data = load_object("Storage/Course_Storage.pkl")
load_task_data_dic = load_object("Storage/Task_Storage.pkl")

# creates new course objects using saved data 
for course_data_tuple in load_course_data:
    new_course = Course(course_data_tuple[0],course_data_tuple[1], left_frame, courses_frame, course_data_tuple[2], icons_dict[course_data_tuple[3]], course_tag)
    course_tag+=1

    course_list.append(new_course)
    new_course.display()

    try:
        tasks_to_be_added = load_task_data_dic[course_data_tuple[4]] # list of tasks to be added to course
        for task_data_tuple in tasks_to_be_added:
            new_course.addTask(n=task_data_tuple[0], d=task_data_tuple[1], dd=task_data_tuple[2])

    except KeyError:
        pass


root.mainloop()

############### POST MAINLOOP ###################
settings_frame.run = False
for course in course_list:

    # find key based on value in icons_dict dictionary
    img_key = next(key for key, value in icons_dict.items() if value == course.icon)
    course_data.append((course.name, course.period, course.color, img_key, course.tag))

task_list = tl.tasks
task_data = {}
for task in task_list:

    try:
        task_data[task.parent_course.tag].append((task.name, task.description, task.due_date))

    except KeyError:
        task_data[task.parent_course.tag] = []
        task_data[task.parent_course.tag].append((task.name, task.description, task.due_date))

# save homework time selection
with open('Storage/Settings_Preferences_Storage.txt', 'w') as text_file:
    text_file.write(settings_frame.homework_time_string + '\n' + settings_frame.name)
    
# saves course data
save_object(course_data, 'Storage/Course_Storage.pkl')
save_object(task_data, "Storage/Task_Storage.pkl")


# Must run by calling main_window.py in command prompt for text to work