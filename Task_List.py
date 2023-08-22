import Task
from tkinter import *
from directory import atlas, colors
import datetime

class Task_List:
    def __init__(self, root):
        self.tasks = []
        self.labels = []
        self.due_date_dic = {}
        self.colors_dic = {}
        self.root = root
        


    def sort(self):
        dates = list(self.due_date_dic.values())
         
        dates = [datetime.datetime.strptime(ts, "%m/%d/%y") for ts in dates]
        dates.sort()
        sorteddates = [datetime.datetime.strftime(ts, "%m/%d/%y") for ts in dates]
        
        for date in sorteddates:
            
            for key in self.due_date_dic:
                if self.due_date_dic[key] == date and not self.tasks.__contains__(key):
                    self.tasks.append(key)
        

    def update(self):
        course_list = atlas[1] # course list added to atlas from main 
        self.tasks.clear()
        self.due_date_dic.clear()
        self.colors_dic.clear()
        for course in course_list:
            for task in course.tasks:
                if task.isExists:
                    self.due_date_dic[task] = datetime.datetime.strftime(datetime.datetime.strptime(task.due_date, "%m/%d/%y"), "%m/%d/%y")
                    
                    self.colors_dic[task] = course.color
        
                #print(task)
        self.sort()
        self.hide()
        self.labels.clear()
        self.display()

    def display(self):
        for task in self.tasks:
            task_label = Label(self.root, text=task.due_date + "  " + task.name+"  ", fg=self.colors_dic[task], bg=colors['center_color'], font='arial 14', image=task.parent_course.icon, compound='right')
            self.labels.append(task_label)
            task_label.grid(sticky='w')

    def hide(self):
        for label in self.labels:
            label.grid_forget()

if __name__ == '__main__':
    ws = Tk()
    ws.title('PythonGuides')

    f = Frame(ws)
    f.grid()
    
    t1 = Task.Task(f)
    t2 = Task.Task(f)
    li = ['8/16/2022','7/15/2022', '12/5/1909']

    tl = Task_List(ws,li)
    tl.sort()
    print(tl.tasks)
    ws.mainloop()

 
