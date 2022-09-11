import tkinter as tk
import time
from tkinter.ttk import Checkbutton, Separator


# TODO implement rest time. and fix reset func

def timer():
    """
    Repeatedly executed and changes the stopwatch timer.
    :Return:None
    """
    global root_after
    global running
    global remaining_rounds

    clock_string_var.set(format_time(time.time() - start_time))
    root_after = root.after(50, timer)
    round_remaining_label['text'] = f'Round remained: {remaining_rounds}'
    if 'selected' in pomodoro_check_button.state():
        _,minute,sec = clock_string_var.get().split(':')
        if sec == '02':
            remaining_rounds -= 1 
            print(remaining_rounds)    
            if remaining_rounds == 0:
                print('run') 
                reset()
            else:
                running = False
                start()



def start():
    """
    Start the stopwatch whenever start button presses.
    nothing happens if the stopwatch already started.
    :return: None
    """
    global running
    global start_time
    global stopped_time
    stopped_time = None

    if not running:
        clock_string_var.set('00:00:00')
        start_time = time.time()
        timer()
        running = True
        toggle_stop_text()
    
def stop_or_continue():
    """
    Stops stopwatch whenever stop button pressed.
    Continues when stop button has already been pressed.
    [stop and continue functionality]
    :return: None
    """
    global running    
    global start_time
    global stopped_time
 
    if running:
        stopped_time = time.time()    
        root.after_cancel(root_after)
        running = False
        toggle_stop_text()
    elif not running and stop_button['text'] == 'CONTINUE':
        # update start_time 
        start_time = time.time() - (stopped_time-start_time)
        timer()
        running = True
        toggle_stop_text()


def reset():
    """
    reset every thing. and set the timer on 00:00:00
    :return: None
    """
    global running
    global remaining_rounds
    if running:
        running = False
        root.after_cancel(root_after)
    stop_button['text'] = 'STOP'
    clock_string_var.set('00:00:00')
    remaining_rounds = variable.get() * 4

def toggle_stop_text():
    """
    Toggle the stop button text to [continue/stop].
    :return: None
    """
    if running:
        stop_button['text'] = 'STOP'
    else:
        stop_button['text'] = 'CONTINUE'
    return 

def format_time(elapsed):
    """
    Returns specified formatted time.
    :param:elapsed: str : string of epoch time
    :Return: str
    """
    hours = int(elapsed/3600)
    minutes = int(elapsed/60 - hours * 60)
    seconds = int(elapsed - hours*3600 - minutes*60)
    return '%02d:%02d:%02d' %(hours, minutes, seconds)


def add_selection_frame():
    """
    Adds some widgets.
    :return: None
    """
    global variable
    global selection_box
    global round_remaining_label
    global selection_label
    global popup_label
    global popup_button
    values = [1,2,3,4,5]
    variable.set(1)
    # if check button selected
    if 'selected' in pomodoro_check_button.state():
        selection_box = tk.OptionMenu(pomodoro_frame, variable,
            *values, command=get_remaining_rounds)
        selection_label = tk.Label(pomodoro_frame,
            text='Choose the number of rounds then\n\
            press "start"')
        selection_label.grid(column=1,row=2)
        selection_box.grid(column=1, row=3, pady=3)
        popup_label = tk.Label(popup_frame, 
            text='Learn about pomodoro?')
        popup_label.grid(column=0, row=0)
        popup_button = tk.Button(popup_frame, text='Click!',
             command=popup_window,width=3)
        popup_button.grid(column=1,row=0, padx=4)

        round_remaining_label = tk.Label(timer_frame,
                text=f'Round remained: {remaining_rounds}',
                fg='red')
        round_remaining_label.grid()
    else:
        selection_box.grid_forget()
        selection_label.grid_forget()
        popup_button.grid_forget()
        popup_label.grid_forget()
        round_remaining_label.grid_forget()
    return None

def get_remaining_rounds(e):
    """
    returns the number of rounds remaining 
    :param: e = event
    :return: string
    """
    global remaining_rounds
    remaining_rounds = variable.get() * 4
    return remaining_rounds


def popup_window():
    """
    opens a popup window contains info about pomodoro technique.
    :return: None
    """

    text = """The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It uses a kitchen timer to break work into intervals, typically 25 minutes in length, separated by short breaks. Each interval is known as a pomodoro, from the Italian word for tomato, after the tomato-shaped kitchen timer Cirillo used as a university student.\nTo learn more see wikipedia page: \"https://en.wikipedia.org/wiki/Pomodoro_Technique\"\n\nIn this app each round contain 4 sub-round which means doing 4 time of 25 minutes on followed by 5 minutes of rest.Then this will going to continue 3 more round and after that you have done if you have choosen '1' in selection box.Also if you have selected more than '1' after 4 sub-round you are going to have a 30 minutes rest.
    """
    top = tk.Toplevel(root)
    top.geometry("650x450")
    top.title("What is \"POMODORO\" technique")
    text_widget = tk.Text(top, font=('Mistral 12 bold'), padx=10,pady=5)
    text_widget.insert(0.0, text)
    text_widget.pack()
    text_widget.tag_add("start", "2.34","3.15")
    text_widget.tag_config("start", foreground= "blue")
    
    return None
    



if __name__ == '__main__':

    running = False
    start_time = None
    stopped_time = None
    root_after = None

    root = tk.Tk(className='Pro StopWatch')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.minsize(300,200)
    clock_string_var = tk.StringVar()
    clock_string_var.set('00:00:00')
    variable = tk.IntVar()
    timer_frame = tk.Frame(master=root, padx=20, pady=10)
    pomodoro_frame = tk.Frame(master=root)
    button_frame = tk.Frame(master=root)
    popup_frame = tk.Frame(master=root)
    timer_frame.grid()
    button_frame.grid()
    pomodoro_frame.grid()
    popup_frame.grid(pady=10)
    remaining_rounds = 4

    # check-box for pomodoro
    pomodoro_check_button = Checkbutton(pomodoro_frame, 
        text='ACTIVATE POMODORO TECHNIQUE',
        command=add_selection_frame, cursor='dot',underline=9)
    pomodoro_check_button.grid(column=1, row=0, pady=5)

    # Actual timer string 
    tk.Label(timer_frame, textvariable=clock_string_var, fg='green',
        justify='center',font=('Times New Roman',50)).grid(row=0,)

    # Buttons
    start_button = tk.Button(button_frame, text='START', command=start)
    stop_button = tk.Button(button_frame, text='STOP', command=stop_or_continue)
    tk.Button(button_frame, text='RESET', command=reset).grid(column=2, row=0)
    start_button.grid(column=0, row=0)
    stop_button.grid(column=1, row=0, padx=5)
    Separator(master=button_frame,
         orient='horizontal').grid(row=1,ipadx=100, pady=10, columnspan=10)

    root.mainloop()