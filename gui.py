import tkinter as tk
from tkinter.ttk import Combobox
import threading
from mixed import start_combined_detection , stop_combined_detection, calibrate_nose
# Global state
isStarted = False


def toggle_start_Stop():
    global isStarted
    global jumpChoice
    global sliderValue
    global sliderBack

    choiceMade = jumpChoice.get()
    sliderValue = 50 - sliderSens.get() / 2
    slideBack =  sliderRef.get() / 100

    if isStarted:
        runningStatus.config(text="Not Running", fg="red")
        MainButton.config(text="Start")
        isStarted = False
        stop_combined_detection()

    else:
        runningStatus.config(text="Running", fg="green")
        MainButton.config(text="Stop")
        isStarted = True
        print(choiceMade)
        threading.Thread(target=start_combined_detection,args=(choiceMade, sliderValue, slideBack), daemon=True).start()
        


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

sliderSens = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Sensitivity", length=200 , variable=tk.IntVar(value=70))

sliderRef = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Cooldown", length=200, variable=tk.IntVar(value=50))
sliderSens.pack(pady=10)
sliderRef.pack(pady=10 )

cal_label = tk.Label(root, text="Calibration will only work after\n starting the application",fg="blue", font=("Arial", 12))
cal_label.pack(pady=10)
calibrateBtn = tk.Button(root, text="Calibrate",command=calibrate_nose, font=("Arial", 12))
calibrateBtn.pack(pady=10)


jumpChoiceLabel = tk.Label(root, text="Jump Action:")
jumpChoiceLabel.pack()
jumpChoice = Combobox(root, values=["Single Blink", "Double Blink"], state="readonly", width=20,)

jumpChoice.current(1)



jumpChoice.pack(pady=10)

root.mainloop()
