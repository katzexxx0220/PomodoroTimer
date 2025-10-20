from tkinter import *
from tkinter import messagebox

class PomodoroTimer:

    def __init__(self):
        # initialize main window
        self.window = Tk()
        self.window.geometry("650x500")
        self.window.title("Pomodoro Timer")
        self.window.configure(bg = '#FCF6D2')

        # create and display menu bar
        menu_bar = Menu(self.window)
        self.window.configure(menu = menu_bar) 

        # add a pull down menu 
        operationMenu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label = "  Select  ", menu = operationMenu)
        operationMenu.add_command(label = "Return To Pomodoro Timer Main Page", command = self.back_previous)

        # timer variables
        self.time_running = False
        self.new_page_created = False
        self.pomodoro_accumulated = False

        # list to track completed session 
        self.completed_sessions = []

        # frame 1: title
        self.frame1 = Frame(self.window, bg = '#FCF6D2')
        self.frame1.pack()
        self.customize_label = Label(self.frame1, text = "Customize Your Time", font = ("Arial", 24, "bold", "italic"), 
                                     bg = '#FCF6D2', fg = '#637A60').pack(pady = 40)

        # frame 2
        self.frame2 = Frame(self.window, bg = '#FCF6D2')
        self.frame2.pack()

        # labels and input stored in list
        texts = ["Focus Time (minutes):", "Break Time (minutes):", "Number of Session(s):"]
        self.input = [StringVar(), StringVar(), StringVar()]
        texts_input = []

        # create input fields
        for i, text in enumerate(texts):
            label = Label(self.frame2, text = text, font = ("Courier", 14, "bold"), bg = '#FCF6D2', fg = '#637A60')
            label.grid(row = i, column = 0, pady = 20)
            entry = Entry(self.frame2, textvariable = self.input[i])
            entry.grid(row = i, column = 1, pady = 20)
            texts_input.append(entry)
        
        # press enter to next input fields
        for i in range(len(texts_input)):
            if i < len(texts_input) - 1:
                texts_input[i].bind("<Return>", lambda event, next_entry = texts_input[i + 1]: next_entry.focus())
            else:
                texts_input[i].bind("<Return>", lambda event: None)

        # enter button
        self.enter = Button(self.window, width = 20, command = self.display_timer, text = "Enter", 
                            font = ("Courier", 14, "bold"), bg = '#B3C58B', fg = '#637A60')
        self.enter.pack(pady = 25)

        self.window.mainloop()
    
    def display_timer(self):   
        '''
        Remove previous frames and buttons
        Convert time to seconds
        Display phase and timer
        '''

        try:        
            # retrieve user input
            focus_time = int(self.input[0].get())
            break_time = int(self.input[1].get())
            session_count = int(self.input[2].get())

            # exception handling to validate input values
            if focus_time <= 0 or break_time <= 0 or session_count <= 0:
                raise ValueError("Please Enter Valid Numbers!")

            if focus_time >= 15:
                raise ValueError("Values Cannot Be Greater Than 999!")

            # convert user input (minutes) to seconds and store in tuple
            self.timer_tuple = (focus_time * 60, break_time * 60, session_count)
            self.remaining_seconds = self.timer_tuple[0]
            self.current_phase = "FOCUS"

            self.frame1.destroy()
            self.frame2.destroy()
            self.enter.destroy()

            self.frame3 = Frame(self.window, bg = '#FCF6D2')
            self.frame3.pack()

            # display current phase
            self.display_phase = Label(self.frame3, text = "{}".format(self.current_phase), font = ("Arial", 20, "bold", "italic"), 
            bg = '#FCF6D2', fg = '#CF7359')
            self.display_phase.pack(pady = 20)

            # display timer
            self.display_time = Label(self.frame3, text = f"{focus_time:02}:00", font = ("Arial", 42, "bold"), bg = '#FCF6D2', 
            fg = '#637A60')
            self.display_time.pack(pady = 35)

            # start button
            self.start_button = Button(self.frame3, width = 10, text = chr(0x25B6), command = self.start_timer, font = 18, bg = '#FCF6D2')
            self.start_button.pack(pady = 20)

            # pause button
            self.pause_button = Button(self.frame3, width = 10, text = chr(0x25A0), command = self.pause_timer, font = 18, bg = '#FCF6D2')
            self.pause_button.pack(pady = 20)

        except ValueError as error:
            messagebox.showerror("Error Message", error)

    # Start countdown timer
    def start_timer(self):
        if not self.time_running: 
            self.time_running = True
            self.update_timer()

    # Pause countdown timer
    def pause_timer(self):
        self.time_running = False

    # Update timer display 
    def update_timer(self):
        if self.time_running and self.remaining_seconds >= 0:
            minutes, seconds = divmod(self.remaining_seconds, 60) # Return quotient and remainder 
            self.display_time.configure(text = f"{minutes:02}:{seconds:02}")
            self.remaining_seconds -= 1 # countdown
            self.window.after(1000, self.update_timer) # Update Timer will be called after 1 second delay

        # Change phase after timer reaches zero
        elif self.remaining_seconds < 0:
            self.change_phase()

    # change phase between focus and break and handle count for completed session(s)
    def change_phase(self):
            match self.current_phase:
                case "FOCUS":
                    self.time_running = False
                    messagebox.showinfo("Time's Up!", "Focus Time's Up!\nPress {} to Continue Break Session".format(chr(0x25B6)))
                    self.current_phase = "BREAK"
                    self.display_phase.configure(text = "BREAK")
                    self.remaining_seconds = self.timer_tuple[1]
                    self.start_button.configure(state = NORMAL)
        
                case "BREAK":
                    self.time_running = False
                    session_number = len(self.completed_sessions) + 1
                    if len(self.completed_sessions) + 1 == self.timer_tuple[2]: # if completed session = input session
                        messagebox.showinfo("Time's Up!", "Break Time's Up!\nPomodoro Completed!") 
                    else: # if completed session less than input session
                        messagebox.showinfo("Time's Up!", "Break Time's Up!\nPress {} to Continue Your Next Session.".format(chr(0x25B6)))

                    # update pomodoro count
                    self.completed_sessions.append(session_number)

                    # display pomodoro count label
                    if self.pomodoro_accumulated:
                        self.pomodoro_accumulated.configure(text = "Pomodoro Count(s): {}".format(session_number))
                    else: 
                        self.pomodoro_accumulated = Label(self.window, text="Pomodoro Count(s): {}".format(session_number), 
                        font = ("Arial", 14, "bold", "italic"), bg = '#FCF6D2', fg = '#637A60')
                        self.pomodoro_accumulated.pack(pady = 20)

                    # start new focus phase if completed session(s) less than input session(s)
                    if len(self.completed_sessions) < self.timer_tuple[2]: 
                        self.current_phase = "FOCUS"
                        self.display_phase.configure(text = "FOCUS")
                        self.remaining_seconds = self.timer_tuple[0]
                    else:
                        self.pomodoro_end() # pomodoro session end 

    # display message and destroy both buttons
    def pomodoro_end(self):
        self.display_time.configure(text = "Pomodoro\nCompleted!", font = ("Arial", 32, "bold", "italic"))
        self.start_button.destroy()
        self.pause_button.destroy()

        # after pomodoro completed given option for users to choose need to continue or not
        if not self.new_page_created:
            self.pomodoro_accumulated.destroy()
            self.new_page = Button(self.window, width = 20, command = self.back_previous, text = "New Page", font = ("Courier", 14, "bold"), 
            bg = '#B3C58B', fg = '#637A60')
            self.new_page.pack(pady = 20)
            self.new_page_created = True

    # return pomodorotimer initial screen
    def back_previous(self):
            self.window.destroy()
            self.__init__()

# Run the application
PomodoroTimer()
