import subprocess
import time


eye_script = "direction.py" 
prediction_script = "prediction.py"


eye_process = subprocess.Popen(["python", eye_script]) 
prediction_process = subprocess.Popen(["python", prediction_script])  

print("✅ Both scripts started successfully!")  

try:
    while True:  
        time.sleep(1)  
except KeyboardInterrupt:
    print("\n🔴 Stopping both scripts...")

  
    eye_process.terminate()   