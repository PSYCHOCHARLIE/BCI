import serial
import joblib
import numpy as np
import pyautogui
import time
import pandas as pd
from scipy.signal import butter, lfilter

# Load model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# Serial connection
ser = serial.Serial('COM7', 115200)
time.sleep(2)

# Bandpass filter settings
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter(data, lowcut=0.5, highcut=50, fs=250, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data)

# Buffer
BUFFER_SIZE = 250  # 1 second at 250Hz
eeg_buffer = []

# Main loop
print("Start reading EEG data...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            eeg_value = float(line)
            eeg_buffer.append(eeg_value)

            if len(eeg_buffer) >= BUFFER_SIZE:
                # Feature Extraction
                buffer_np = np.array(eeg_buffer[-BUFFER_SIZE:])
                filtered = apply_bandpass_filter(buffer_np)
                mean_val = np.mean(filtered)
                std_val = np.std(filtered)
                max_val = np.max(filtered)
                min_val = np.min(filtered)
                peak_to_peak = max_val - min_val

                # Create DataFrame with correct feature names
                X = pd.DataFrame([{
                    'mean': mean_val,
                    'std': std_val,
                    'max': max_val,
                    'min': min_val,
                    'ptp': peak_to_peak
                }])

                # Scale
                X_scaled = scaler.transform(X)

                # Predict
                prediction = model.predict(X_scaled)[0]

                print(f"Prediction: {prediction}")

                if prediction == 1:
                    pyautogui.press('w')  # Simulate key press

                eeg_buffer = []

    except Exception as e:
        print("Error:", e)
        continue
