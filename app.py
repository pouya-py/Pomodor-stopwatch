import tkinter as tk
import time
from tkinter.ttk import Checkbutton, Separator
from utils import format_time

# TODO implement rest time. and fix reset func

def timer():
    """
    Repeatedly will be executed and changes the stopwatch timer.
    :Return:None
    """
    global root_after
    clock_string_var.set(format_time(time.time() - start_time))
    root_after = root.after(5, timer)
    if 'selected' in pomodoro_check_button.state():
        if remaining_rounds > 0:
            update_rounds()
        else:
            reset()

def update_rounds():
    global running
    global remaining_rounds
    global round_remaining_label
    _, minute, sec = clock_string_var.get().split(':')
    if sec in ['03',]:
        remaining_rounds -= 1 
        round_remaining_label['text'] = f'{remaining_rounds} from total of {variable.get()*4}'
        print(remaining_rounds)
        if remaining_rounds <= 0:
            round_remaining_label['text'] = f'0 from total of {variable.get()*4}'
            stop_or_continue()

def start():
    """
    Start the stopwatch whenever start button pressed.
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
    # disable level selection
    if selection_box:
        selection_box.configure(state='disabled')

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
    if remaining_rounds <= 0:
        return
    if running:
        # stop the timer
        stopped_time = time.time()    
        root.after_cancel(root_after)
        running = False
        toggle_stop_text()
    elif not running and stop_button['text'] == 'CONTINUE':
        # continue the timer
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
    global round_remaining_label
    if running:
        running = False
        root.after_cancel(root_after)
    stop_button['text'] = 'STOP'
    clock_string_var.set('00:00:00')
    remaining_rounds = int(variable.get()) * 4
    if selection_box:
        round_remaining_label['text'] = f'{remaining_rounds} from total of {variable.get()*4}'
        selection_box.configure(state='active')
        selection_box.focus_force()

def toggle_stop_text():
    """
    Toggle the stop button text to continue/stop.
    :return: None
    """
    if running:
        stop_button['text'] = 'STOP'
    else:
        stop_button['text'] = 'CONTINUE'
    return 


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
    LEVELS = [1,2,3,4,5]
    variable.set(1)
    # if check button selected
    if 'selected' in pomodoro_check_button.state():
        selection_box = tk.OptionMenu(pomodoro_frame, variable,
            *LEVELS, command=set_remaining_rounds_label)
        selection_label = tk.Label(pomodoro_frame,
            text='Choose your level and press "start"')
        selection_label.grid(column=1,row=2)
        selection_box.grid(column=1, row=3, pady=3)
        popup_label = tk.Label(popup_frame, 
            text='Learn about pomodoro?')
        popup_label.grid(column=0, row=0)
        popup_button = tk.Button(popup_frame, text='Click!',
             command=popup_window,width=3)
        popup_button.grid(column=1,row=0, padx=4)

        round_remaining_label = tk.Label(timer_frame,
                text=f'{remaining_rounds} from total of {variable.get()*4}',
                fg='red')
        round_remaining_label.grid()


    else:
        selection_box.grid_forget()
        selection_label.grid_forget()
        popup_button.grid_forget()
        popup_label.grid_forget()
        round_remaining_label.grid_forget()
    return 

def set_remaining_rounds_label(e):
    """
    returns the number of rounds remaining 
    :return: str
    """
    global round_remaining_label
    round_remaining_label['text'] = f'{variable.get()*4} from total of {variable.get()*4}'
    


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
    return 
    



if __name__ == '__main__':

    running = False
    selection_box = None

    root = tk.Tk(className='Pro StopWatch')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.minsize(300,200)
    # set a global tk string variable
    clock_string_var = tk.StringVar()
    clock_string_var.set('00:00:00')
    # set a global tk integer variable
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
    # the timer string 
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