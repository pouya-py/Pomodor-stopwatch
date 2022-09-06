import tkinter as tk
import time


running = False
start_time = None
stopped_time = None
duration_stopped= 0
root_after = None

root = tk.Tk(className='Pro StopWatch')
clock_string_var = tk.StringVar()
clock_string_var.set('00:00:00')
frame = tk.Frame(master=root, padx=20, )
button_frame = tk.Frame(master=root, padx=20, pady=20)
button_frame.grid()
frame.grid()



def timer():
    global root_after
    global start_time
    if stopped_time:
        # breakpoint()
        clock_string_var.set(format_time((time.time()- (stopped_time + duration_stopped)) + (stopped_time-start_time)))

    else:
        clock_string_var.set(format_time(time.time() - start_time))
    root_after = root.after(50, timer)



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
        start_time = time.time()
        timer()
        running = True
        toggle_stop_text()
    
def stop():
    """
    Stops stopwatch whenever stop button pressed.
    :return: None
    """
    global running    
    global start_time
    global stopped_time
    global duration_stopped

    if running:
        stopped_time = time.time()    
        root.after_cancel(root_after)
        running = False
        toggle_stop_text()
    elif not running and stop_button['text'] == 'CONTINUE':
        duration_stopped =  time.time() - stopped_time
        timer()
        running = True
        toggle_stop_text()


def reset():
    """
    reset every thing. and set the timer on 00:00:00
    :return: None
    """
    global stopped_time
    global running
    if running:
        running = False
        root.after_cancel(root_after)
    stop_button['text'] = 'STOP'
    clock_string_var.set('00:00:00')
    stopped_time = None

def toggle_stop_text():
    """
    Toggle the stop button text to [continue] and reverse.
    :return: None
    """
    if running:
        stop_button['text'] = 'STOP'
    else:
        stop_button['text'] = 'CONTINUE'
    return 

def format_time(elapsed):
    hours = int(elapsed/3600)
    minutes = int(elapsed/60 - hours * 60)
    seconds = int(elapsed - hours*3600 - minutes*60)
    return '%02d:%02d:%02d' %(hours, minutes, seconds)


def start_pomodor():
    return

start_button = tk.Button(button_frame, text='START', command=start)

stop_button = tk.Button(button_frame, text='STOP', command=stop)
# stop_button.bind('<Button-1>', toggle_stop_text())

tk.Button(button_frame, text='RESET', command=reset).grid(column=2, row=0)


start_button.grid(column=0, row=0)
stop_button.grid(column=1, row=0, padx=5)

# Create space
tk.Label(frame, text='  ').grid(row=1)
# check-box for pomodor
tk.Checkbutton(frame, text='ACTIVATE POMODOR TECHNIQUE',
     command=start_pomodor, cursor='dot', justify='center',
     height=2, underline=9,).grid(column=1, row=2)

tk.Label(frame, textvariable=clock_string_var, fg='green',
     justify='center',font=('Times New Roman',50)).grid(column=1, row=3)
     

root.mainloop()