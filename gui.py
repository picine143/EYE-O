import tkinter as tk
from tkinter.ttk import Combobox
from blink_only import *

# Global state
isStarted = False  # This will persist across button clicks

def toggle_start_Stop():
    global isStarted
    if isStarted:
        runningStatus.config(text="Not Running", fg="red")
        MainButton.config(text="Start")
        isStarted = False
        start_blink_detection(isStarted)
        
    else:
        runningStatus.config(text="Running", fg="green")
        MainButton.config(text="Stop")
        isStarted = True
        start_blink_detection(isStarted)
            
        

# Create main window
root = tk.Tk()
root.title("Ctrl I")
root.geometry("300x600")

# Create widgets
Header = tk.Label(root, text="Welcome to Ctrl I", font=("Arial", 16))
Header.pack()

description = tk.Label(root, text="This is an app that lets you play games\nwithout using your hand.", font=("Arial", 12))
description.pack()

MainButton = tk.Button(root, text="Start", command=toggle_start_Stop, font=("Arial", 14), width=10, height=2)
MainButton.pack(pady=10)

# Running status label (persistent)
runningStatus = tk.Label(root, text="Not Running", font=("Arial", 12), fg="red")
runningStatus.pack()

sliderSens = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Sensitivity", length=200)
sliderRef = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Refresh Rate", length=200)
sliderSens.pack(pady=10)
sliderRef.pack(pady=10)

jumpChoiceLabel = tk.Label(root, text="Jump Action:")
jumpChoiceLabel.pack()
jumpChoice = Combobox(root, values=["Single Blink" , "Double Blink"] , state="readonly", width=20)
jumpChoice.current(1)  # Set default value
jumpChoice.pack(pady=10)

# Run the GUI event loop
root.mainloop()
