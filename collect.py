import serial
import csv
import time
import datetime  

COM_PORT = 'COM7'  
BAUD_RATE = 115200  


ser = serial.Serial(COM_PORT, BAUD_RATE)


with open('shatya.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    
    max_duration = 900

    start_time = time.time()

    print("Collecting data...")

    while time.time() - start_time < max_duration:
        
        data = ser.readline().decode("latin-1").strip()

    
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        
        values = data.split(',')

        if len(values) > 0  and values[0].isdigit():
            
            csvwriter.writerow([current_time, values[0]])

ser.close()
