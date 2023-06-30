import random
import tkinter as tk
import os
from win32api import GetMonitorInfo, MonitorFromPoint
import win32gui
import datetime
import csv

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")

window = tk.Tk()
lastClickX = 0
lastClickY = 0
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
global drag
drag = False # gives error, but i need it
global falling
falling = False # gives error, but i need it
idle_num = [x for x in range(10)]
sit_num = [x for x in range(15, 20)]
walk_left = [x for x in range(10, 12)]
walk_right = [x for x in range(12, 15)]
impath = f"{os.getcwd()}\\cats\\"


# REWORK NEEDED but this will do for now
class TextBox(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.image = tk.PhotoImage(file=impath + 'chatbox.png')
        self.text_box = tk.Label(self, bd=0, bg='black', image=self.image, compound='center', fg="#ffffff",
                                 font=("Aleo", 22), cursor="hand2")
        self.text_box.pack()
        self.text_box.place(relwidth=1, relheight=1)
        ######################################################################################
        self.text_box['text'] = "Time for class!"
        ######################################################################################
        self.hiding = False
        self.hide()
        self.text_box.bind('<Button-1>', func=self.hide)

    def set_text(self, text):
        self.text_box['text'] = text

    def hide(self, mouse=None):
        if not self.hiding:
            self.text_box.place(relx=1, relwidth=1, relheight=1)
            self.hiding = True

    def show(self):
        if self.hiding:
            self.text_box.place(relx=0, relwidth=1, relheight=1)
            self.hiding = False

# new to prepare a whole new UI box for the scheduling

class Task:
    """Stores the day of the week, time, and zoom link"""
    name: str
    time: datetime.datetime
    info: str

    def __init__(self, name: str, time: datetime.datetime, info: str):
        self.name = name
        self.time = time
        self.info = info


def make_schedule():
    tasks_so_far = []
    now = datetime.datetime.now()
    with open('schedule.csv', newline='') as file:
        r = csv.reader(file)

        # puts them into the list if they have a time
        row = next(r)
        for data in row:
            if data != '':
                task = data.split(',')
                task_time = now.replace(hour=int(task[1].split(':')[0]), minute=int(task[1].split(':')[1]))
                if now < task_time:
                    name = task[0].strip()
                    time = task_time
                    info = task[2].strip()
                    tasks_so_far.append(Task(name, time, info))
    return tasks_so_far


# add to schedule function
def add_to_schedule(tasks_so_far):
    """Adds to the csv as well as modified the UI accordingly"""
    # maybe the UI work is best done in another function 
    # do something about duplicate names

    return

def remove_from_schedule(tasks_so_far, task_name):
    """Removes from the csv as well as modify the UI accordingly"""
    # maybe the UI work is best done in another function 

    return

# reorder tasks list function
def reorder_schedule():

    return


def start():
    """Start off animation (which i gave up on implementing) and logistics"""
    todo = make_schedule()
    text_box.set_text("MEOW!!!")
    text_box.show()
    update(0, 1000, 'left', 0, screen_width - 400, work_area[3] - 475, 5, todo)


# transfer random no. to event
def pet_status(event_number: int) -> tuple[str, int]:
    space = 500
    status = None

    if event_number in idle_num:
        status = 'idle'
    elif event_number in walk_left:
        status = 'left'
    elif event_number in walk_right:
        status = 'right'
    elif event_number in sit_num:
        status = 'sit'
    return status, space


# release the pet
def release(event):
    global drag
    drag = False
    global new_x, new_y
    new_x = event.x - lastClickX + window.winfo_x()
    new_y = event.y - lastClickY + window.winfo_y()
    global falling
    falling = True


# gif looper
def gif_work(mode: str, cycle: int, ran):
    """This makes the user make it move"""
    if mode == 'drag':
        if cycle < len(drag_animations[ran]) - 1:
            label.configure(image=drag_animations[ran][cycle])
            cycle += 1
        else:
            cycle = 0
    else:
        if cycle < len(animations[mode]) - 1:
            label.configure(image=animations[mode][cycle])
            cycle += 1
        else:
            if mode == 'prep':
                mode = 'watch'
            cycle = 0
    return cycle, mode


def movement(mode: str, x: int) -> int:
    """Handles the movement"""
    if mode == 'left':
        if x > - 550:
            x -= 2
        else:
            x = screen_width - 400
    elif mode == 'right':
        if x < screen_width - 400:
            x += 2
        else:
            x = -550
    return x


def save_last_click(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y
    global drag
    drag = True


def dragging(event):
    global x
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x, y))


def update(counter_so_far, again, mode, cycle, x, y, ran, todo):
    """This keeps updating to look for inputs, if non, just use event to determine animation"""
    # modules is such a beautiful operation
    if counter_so_far % 5 == 0:
        cycle, mode = gif_work(mode, cycle, ran)
    x = movement(mode, x)
    mode = foreground_check(mode)

    if not drag:
        global falling
        if falling:
            x = new_x
            y = new_y
            counter_so_far = again
            falling = False
            ran = 5
        if counter_so_far >= again:
            if mode not in {'class', 'watch', 'prep'}:
                mode, again = pet_status(random.randint(0, 19))
            counter_so_far = 0
        window.geometry('500x500+' + str(x) + f'+{y}')
    else:
        mode = 'drag'
        if ran == 5:
            ran = random.randint(0, 2)
    counter_so_far += 1
    window.after(10, update, counter_so_far, again, mode, cycle, x, y, ran)


def event_checker(schedule: list[Task]):
    """Checks if it's time for class every 10 mins"""
    if (schedule[0].time - datetime.timedelta(minutes=1)) <= datetime.datetime.now() <= schedule[0].time:
        # she tells u to join class
        text_box.set_text("Time for " + schedule[0].name + "!\n" + schedule[0].info)
        text_box.show()
        schedule.pop(0)

    if schedule:
        window.after(60000, event_checker, schedule)


def farewell(event):
    goodbyes = ["You'll.... regret..this.....", "Remember to turn me back on again, OK?"]
    text_box.set_text(random.choice(goodbyes))
    text_box.show()
    window.after(2000, window.destroy)


# put da gifs (pronounced like gift without the t) into da list
idle = [tk.PhotoImage(file=impath + 'idle.gif', format='gif -index %i' % i) for i in range(64)]  # idle gif
sleep = [tk.PhotoImage(file=impath + 'scrub.gif', format='gif -index %i' % i) for i in range(15)]  # sleep gif
walk_positive = [tk.PhotoImage(file=impath + 'walking_pos.gif', format='gif -index %i' % i) for i in
                 range(11)]  # walk to left gif
walk_negative = [tk.PhotoImage(file=impath + 'walking_neg.gif', format='gif -index %i' % i) for i in
                 range(11)]  # walk to right gif
in_class = [tk.PhotoImage(file=impath + 'class.gif', format='gif -index %i' % i) for i in range(2)]  # class gif
watch = [tk.PhotoImage(file=impath + 'watch.gif', format='gif -index %i' % i) for i in range(19)]  # watch gif
prep = [tk.PhotoImage(file=impath + 'chairpop.gif', format='gif -index %i' % i) for i in range(20)]  # idle gif
# we put all the animations in a dict, i think this is a good idea(?)
animations = {'idle': idle, 'right': walk_negative, 'left': walk_positive, 'sit': sleep, 'class': in_class,
              'watch': watch, 'prep': prep}

# drag variations
drag1 = [tk.PhotoImage(file=impath + 'low.gif', format='gif -index %i' % i) for i in range(18)]
drag2 = [tk.PhotoImage(file=impath + 'lowlow.gif', format='gif -index %i' % i) for i in range(26)]
drag3 = [tk.PhotoImage(file=impath + 'lowlowlow.gif', format='gif -index %i' % i) for i in range(18)]
drag_animations = [drag1, drag2, drag3]

# window configuration
window.config(highlightbackground='black')
window.config(background='black')
window.attributes('-topmost', True)
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
label.pack()
label.place(x=350, y=350)
text_box = TextBox(window, bd=0, bg="black")
text_box.pack()
text_box.place(relwidth=1, relheight=0.7)


def foreground_check(mode):
    temp_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if 'YouTube' in temp_window_name:
        if not mode == 'watch':
            mode = 'prep'
    elif mode in {'watch'} and temp_window_name not in {'Chat', 'tk'}:
        mode = 'idle'
    return mode


# button binds
label.bind('<Button-1>', save_last_click)
label.bind('<B1-Motion>', dragging)
label.bind('<ButtonRelease-1>', release)
label.bind('<Button-3>', farewell)

# here goes nothing
start()
window.mainloop()
