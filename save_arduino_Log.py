import os
import serial
from datetime import datetime, timedelta
#把換port放上去了,我這邊OK了,謝
script_dir = os.path.dirname(os.path.abspath(__file__))
# 
# Establish a serial connection to the Arduino
try:
    ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's serial port
except:
    print("change to COM6 ")
    ser = serial.Serial('COM6', 9600)  # Replace 'COM3' with your Arduino's serial port
flag=1
start_time = datetime.now()
while flag:
    if datetime.now() - start_time > timedelta(minutes=1):
        print("1 minute has passed. Stopping the loop.")
        flag=0
    if ser.in_waiting > 0:
        
            flag=1
            # Read the message from Arduino
            message = ser.readline().decode().strip()
        
            # Extract the time from the message
        
            current_time = message.split("Current time: ")[0]

            # Create directory with current date
            now = datetime.now()
             
            date = now.strftime("%Y%m%d")
            now_time= now.strftime("%H")
            now_time2 =now.strftime("%Y%m%d%H%M")
            directory = os.path.join(script_dir, date,"")
            print(directory)
            # Check if directory exists, if not, create it
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            # Create filename with current date and Arduino time
            filename = os.path.join(directory,f"{date}_{now_time}.txt")
            print(filename)
            # Write the message to the file
            with open(filename, 'a') as file:
                file.write(message +now_time2+'\n')

            print(f"Message '{message}' written to {filename}")
