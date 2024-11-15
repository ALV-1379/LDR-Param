import serial
import time
import tkinter as tk
from tkinter import Canvas

#serial port 
ser = serial.Serial('COM3', 9600)
time.sleep(0)  # wait time for get connection 

# make ui
root = tk.Tk()
root.title("LDR LED Control")
root.geometry("400x250") 
root.configure(bg="#2c3e50")  



#lable
title_label = tk.Label(root, text="LDR LED Control", font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50")
title_label.pack(pady=10)

#show  now light
brightness_label = tk.Label(root, text="Brightness Level: 0", font=("Helvetica", 12), fg="white", bg="#2c3e50")
brightness_label.pack(pady=5)



#make leds
canvas = Canvas(root, width=300, height=100, bg="#2c3e50", highlightthickness=0)
canvas.pack()

#show ldr parametrs
ldr_label = tk.Label(root, text="LDR Value: 0", font=("Helvetica", 12), fg="white", bg="#2c3e50")
ldr_label.pack(pady=5)


# make 5 virtual led
leds = []
for i in range(5):
    led = canvas.create_oval(10 + i * 60, 30, 50 + i * 60, 70, fill="#34495e", outline="#2c3e50", width=2)
    leds.append(led)

# exit btn
exit_button = tk.Button(root, text="Exit", font=("Helvetica", 10), command=root.quit, bg="#e74c3c", fg="white", relief="flat")
exit_button.pack(pady=10)


# change led mode from parametrs
def update_leds(brightness):
    brightness_label.config(text=f"Brightness Level: {brightness}")
    for i in range(5):
        color = "#f1c40f" if i < brightness else "#34495e"  # زرد برای LED روشن و خاکستری برای LED خاموش
        canvas.itemconfig(leds[i], fill=color)


# make a stage for leds from ldr value
def map_ldr_to_brightness(ldr_value):
    if ldr_value < 50:
        return 0
    elif ldr_value <= 200:
        return 1
    elif ldr_value <= 400:
        return 2
    elif ldr_value <= 600:
        return 3
    elif ldr_value <= 800:
        return 4
    else:
        return 5

#  read param from Arduino
def read_from_arduino():
    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        
        #log param
        print("Received line:", line)
        
        try:
            #make ldr value to int
            ldr_value = int(line)
            brightness = map_ldr_to_brightness(ldr_value)
            update_leds(brightness)
            ldr_label.config(text=f"LDR Value: {ldr_value}")  # show ldr val in ui
        except ValueError:
            print("خطا: مقدار دریافتی عددی نیست:", line)
    
    root.after(500, read_from_arduino)  # update in .5 sec

#start read from Arduino
read_from_arduino()

#make ui
root.mainloop()

