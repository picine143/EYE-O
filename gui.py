import tkinter as tk
from tkinter.ttk import Combobox
import threading
from blink_only import start_blink_detection, stop_blink_detection

# Global state
isStarted = False


def toggle_start_Stop():
    global isStarted
    global jumpChoice

    choiceMade = jumpChoice.get()
    if isStarted:
        runningStatus.config(text="Not Running", fg="red")
        MainButton.config(text="Start")
        isStarted = False
        stop_blink_detection(choiceMade)

    else:
        runningStatus.config(text="Running", fg="green")
        MainButton.config(text="Stop")
        isStarted = True
        print(choiceMade)
        threading.Thread(target=start_blink_detection, daemon=True).start()

# Create main window
root = tk.Tk()
root.title("Ctrl I")
root.geometry("300x600")

# UI Elements
Header = tk.Label(root, text="Welcome to Ctrl I", font=("Arial", 16))
Header.pack()

description = tk.Label(root, text="This is an app that lets you play games\nwithout using your hand.", font=("Arial", 12))
description.pack()

MainButton = tk.Button(root, text="Start", command=toggle_start_Stop, font=("Arial", 14), width=10, height=2)
MainButton.pack(pady=10)

runningStatus = tk.Label(root, text="Not Running", font=("Arial", 12), fg="red")
runningStatus.pack()

sliderSens = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Sensitivity", length=200)
sliderRef = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Refresh Rate", length=200)
sliderSens.pack(pady=10)
sliderRef.pack(pady=10)

jumpChoiceLabel = tk.Label(root, text="Jump Action:")
jumpChoiceLabel.pack()
jumpChoice = Combobox(root, values=["Single Blink", "Double Blink"], state="readonly", width=20,)

jumpChoice.current(1)



jumpChoice.pack(pady=10)

root.mainloop()
