import tkinter as tk
from time import strftime, localtime
from tkinter import simpledialog, messagebox
import sys
import math
import json

# Function to update the time
def update_time():
    current_time = strftime("%H:%M:%S", localtime())
    time_label.config(text=current_time)
    update_clock_face()
    root.after(100, update_time)  # Update every 100 milliseconds

# Function to update the clock face
def update_clock_face():
    current_time = strftime("%H:%M:%S", localtime())
    hours, minutes, seconds = map(int, current_time.split(':'))

    seconds_angle = (seconds / 60) * 360
    minutes_angle = (minutes / 60) * 360
    hours_angle = ((hours % 12) / 12) * 360 + (minutes / 60) * 30

    update_hand(seconds_hand, seconds_angle, 90, "red", 1)
    update_hand(minutes_hand, minutes_angle, 70, "black", 3)
    update_hand(hours_hand, hours_angle, 50, "black", 5)

# Function to update a hand of the clock
def update_hand(hand, angle, length, color, width):
    x_center, y_center = 200, 200
    angle = math.radians(angle) - math.pi / 2
    x_end = x_center + length * math.cos(angle)
    y_end = y_center + length * math.sin(angle)
    canvas.coords(hand, x_center, y_center, x_end, y_end)
    canvas.itemconfig(hand, fill=color, width=width)

# Function to add an event using the current time
def add_event():
    current_time = strftime("%H:%M:%S", localtime())
    event_text = simpledialog.askstring("Input", "Enter your event:")
    if event_text:
        events[current_time] = event_text
        save_events_to_file()
        messagebox.showinfo("Event Added", f"Event added for {current_time}")

# Function to check for events
def check_events():
    current_time = strftime("%H:%M:%S", localtime())
    if current_time in events:
        messagebox.showinfo("Event", f"Event for {current_time}: {events[current_time]}")
    root.after(1000, check_events)

# Function to view previous events
def view_previous_events():
    all_events = "\n".join(f"{time}: {event}" for time, event in events.items())
    messagebox.showinfo("Previous Events", all_events if all_events else "No previous events.")

# Function to exit the application
def exit_app():
    root.destroy()
    sys.exit()

# Function to save events to a file
def save_events_to_file():
    with open("events.json", "w") as file:
        json.dump(events, file)

# Function to load events from a file
def load_events_from_file():
    global events
    try:
        with open("events.json", "r") as file:
            events = json.load(file)
    except FileNotFoundError:
        events = {}

# Create the main window using tkinter
root = tk.Tk()
root.title("Clock with Events")
root.configure(bg="white")  # Set the background color to white

# Create canvas for the clock
canvas = tk.Canvas(root, width=400, height=400, bg=None)  # Set background to None
canvas.pack()

# Clock face with hour marks
canvas.create_oval(50, 50, 350, 350, outline="black", width=2)
for i in range(12):
    angle = math.radians(i * 30 - 90)
    x_start = 200 + 140 * math.cos(angle)
    y_start = 200 + 140 * math.sin(angle)
    x_end = 200 + 160 * math.cos(angle)
    y_end = 200 + 160 * math.sin(angle)
    canvas.create_line(x_start, y_start, x_end, y_end, fill="black", width=2)

# Clock hands
seconds_hand = canvas.create_line(200, 200, 200, 100, width=1, fill="red")
minutes_hand = canvas.create_line(200, 200, 200, 120, width=3, fill="black")
hours_hand = canvas.create_line(200, 200, 200, 140, width=5, fill="black")

# Display the time
time_label = tk.Label(root, font=("Helvetica", 20, "bold"), bg="white")
time_label.pack(pady=20)

# Add buttons to add events, view previous events, and exit
add_event_button = tk.Button(root, text="Add Event", command=add_event, font=("Helvetica", 14), bg="white")
add_event_button.pack(pady=10)

view_events_button = tk.Button(root, text="View Previous Events", command=view_previous_events, font=("Helvetica", 14), bg="white")
view_events_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app, font=("Helvetica", 14), bg="white")
exit_button.pack(pady=10)

# Dictionary to store events
events = {}

# Load events from file
load_events_from_file()

# Start the clock and events checker
update_time()
check_events()

# Run the application
root.mainloop()