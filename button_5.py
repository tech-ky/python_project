import tkinter as tk
from tkinter import Frame, Label, Entry, Button, StringVar
from threading import Thread
import random

# Global Variables
Bus_list = []
buses = []
notification_labels = []
running = False
number_of_bus = 0
User_Bus_choice = None  # Initialize User_Bus_choice globally

def GUI(user_bus_choice):  # Receive User_Bus_choice as a parameter
    global window, User_Bus_choice
    User_Bus_choice = user_bus_choice  # Assign to global variable
    window = tk.Tk()
    window.title("Bus Simulator")
    window.geometry('1050x820')
    window.resizable(False, False)

    #***************************Simulation Frame***************************
    class Bus:
        def __init__(self, canvas, x, y, width, height, label, speed):
            self.canvas = canvas
            self.rect = canvas.create_rectangle(
                x, y, x + width, y + height,
                fill='Green', 
                outline='black')
            self.text = canvas.create_text(
                x + width / 2, y + height / 2, text=label,
                fill='white',
                font=('Times New Roman', 10, 'bold'))
            self.label = label
            self.speed = speed
            
        def move(self, dx=0, dy=None):
            if dy is None:
                dy = self.speed
            self.canvas.move(self.rect, dx, dy)
            self.canvas.move(self.text, dx, dy)

    def create_bus(bus_number):
        x = 10 + len(buses) * 45
        y = 10
        bus_width = 30
        bus_height = 50
        bus_speed = random.randint(2, 10)
        
        bus = Bus(canvas, x, y, bus_width, bus_height, bus_number, bus_speed)
        buses.append(bus)

    # Frame
    Simulation_frame = Frame(master=window, width=750, height=800, highlightbackground='blue', highlightthickness=3)
    Simulation_frame.pack(side='left', expand=True, padx=10, pady=10, ipadx=10, ipady=10)

    # Widget
    global canvas
    canvas = tk.Canvas(Simulation_frame, width=635, height=700, background="#789")
    message_title = Label(Simulation_frame, text="Bus Simulation", fg="black", font=('Helvetica', 16, 'bold underline'))

    # Design Canvas
    border = 2
    dotted_lines = 25
    canvas.create_line(dotted_lines, 0, dotted_lines, 800, fill="white", width=5, dash=(60,30))
    for i in range(13):
        border += 45
        canvas.create_line(border, 0, border, 800, fill="black", width=3,)
        dotted_lines += 45
        canvas.create_line(dotted_lines, 0, dotted_lines, 800, fill="white", width=5, dash=(60,30))
    canvas.create_rectangle(0, 650, 680, 670, outline="black", fill="blue", width=2)
    canvas.create_text(340, 660, text="BUS STOP", font=('Helvetica', 12, 'bold'), fill='white')

    # Grid
    Simulation_frame.rowconfigure((0, 1), weight=1)
    Simulation_frame.columnconfigure((0), weight=1)

    canvas.grid(row=1, column=0)
    message_title.grid(row=0, column=0)

    #***************************Bus List Frame***************************
    # Variable
    string_var = StringVar()

    # Functions
    def Add_Bus_Function(): 
        global number_of_bus
        if number_of_bus < 14:
            try:
                User_Input = int(string_var.get())
                if isinstance(User_Input, int) and 0 <= User_Input < 1000: 
                    message_output.config(text=f"Added {User_Input} to Bus_list.", fg="green") 
                    Bus_list.append(User_Input)
                    create_bus(User_Input)
                    number_of_bus += 1
                    update_notification_labels()  # Update notification labels after adding bus
                else:
                    message_output.config(text="Please enter an integer \nless than 4 digits.", fg="red")
            except ValueError:
                message_output.config(text="Please enter a valid integer \nless than 4 digits.", fg="red")
        else:
            message_output.config(text="Exceed maximum number of inputs", fg="red")

    def update_notification_labels():
        for i in range(len(notification_labels)):
            if i < len(buses):
                bus_number = buses[i].label
                bus_speed = buses[i].speed
                notification_labels[i].config(text=f"Bus {bus_number} Speed: {bus_speed}", bg="white")
            else:
                notification_labels[i].config(text="", bg="white")

    def start_function():
        global running
        message_output.config(text="Simulation has started", fg="black")
        running = True
        move_buses()

    def stop_function():
        global running
        message_output.config(text="Simulation has stopped", fg="black")
        running = False

    def move_buses():
        if running:
            for bus in buses:
                bus.move()
                update_notification_background()
                check_bus_arrival(bus)
                check_user_bus_arrival()
            window.update()
            window.after(50, move_buses)

    # Frame
    Control_frame = Frame(master=window, width=200, height=200, highlightbackground='blue', highlightthickness=3)
    Control_frame.pack(side='top', expand=True, padx=20, pady=20, ipadx=20, ipady=20)
    Control_frame.pack_propagate(False)

    # Widget
    Bus_list_Entry = Entry(Control_frame, textvariable=string_var)
    Add_Button = Button(Control_frame, text="Add Bus", command=Add_Bus_Function)
    message_output = Label(Control_frame, text="", fg="black", font=('Helvetica', 10, 'bold'))
    Start_Button = Button(Control_frame, text="Start", command=start_function, bg='green')
    Stop_Button = Button(Control_frame, text="Stop", command=stop_function, bg='red')

    # Grid
    Bus_list_Entry.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    Add_Button.grid(row=0, column=3, columnspan=1, sticky="nsew", padx=5, pady=5)
    Start_Button.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    Stop_Button.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)
    message_output.grid(row=3, column=0, columnspan=4, sticky="nsew")

    #***************************Notify Driver Frame***************************
    # Functions
    def check_user_bus_arrival():
        global User_Bus_choice
        for bus in buses:
            if int(bus.label) == int(User_Bus_choice) and bus.canvas.coords(bus.rect)[1] >= 650:
                for label in notification_labels:
                    label.config(bg="white")
                break

    def check_bus_arrival(bus):
        if bus.canvas.coords(bus.rect)[1] >= 650:
            bus_index = buses.index(bus)
            if 0 <= bus_index < len(notification_labels):
                notification_label = notification_labels[bus_index]
                notification_label.config(text="")

    def update_notification_background():
        global User_Bus_choice
        for i in range(len(buses)):
            if int(buses[i].label) == int(User_Bus_choice):
                notification_labels[i].config(bg="yellow")
            else:
                notification_labels[i].config(bg="white")

    # Frame
    Notify_Driver_frame = Frame(master=window, width=200, height=700, highlightbackground='blue', highlightthickness=3)
    Notify_Driver_frame.pack(side='top', expand=True ,padx=10)
    Notify_Driver_frame.pack_propagate(False)

    # Create notification labels for each bus
    for i in range(14):
        notification_label = Label(Notify_Driver_frame, text=f"Bus {i+1} Speed: -", bg="white", height=2, width=20, relief="solid")
        notification_labels.append(notification_label)
        notification_label.grid(row=i // 2, column=i % 2, padx=5, pady=5)

    # Start the Tkinter main loop
    window.mainloop()

def main():
    global User_Bus_choice
    User_key_pad_Input = input("Please Enter Input:\n")
    User_Bus_choice = ''.join(map(str, User_key_pad_Input))  # Assign User_Bus_choice

    GUI(User_Bus_choice)
    
if __name__ == '__main__':
    main()
