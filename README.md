# BCI PROJECT mind

This repository implements a Brain-Computer Interface (BCI) system using the Bioamp EXG Pill (single-channel EEG amplifier) for real-time brain signal acquisition, processing, and computer control.

---

## Introduction

**BCI PROJECT mind** is a Python-based platform for brain-computer interfacing, designed to:
- Acquire EEG signals using the Bioamp EXG Pill and an ESP32/Arduino microcontroller.
- Process and analyze brain signals in real time.
- Predict user intent using machine learning models.
- Enable hands-free computer control (e.g., simulating key presses).
- Visualize EEG frequency bands and support eye-tracking for richer interaction.

---

## Hardware Requirements
- **Bioamp EXG Pill** (single-channel EEG/EMG/ECG amplifier)
- **ESP32 or Arduino** (for digitizing and transmitting EEG data)
- **PC with Python 3.x**
- (Optional) **Webcam** (for eye-tracking features)

---

## Project Structure

```
PROJECT/
│
├── collect.py              # Script to collect EEG data from serial and save to CSV
├── prediction.py           # Real-time EEG processing and intent prediction (main BCI script)
├── prediction2.py          # Alternative prediction script with different features/model
├── direction.py            # Eye-tracking script for left/right gaze detection and key simulation
├── visuale.py              # Real-time EEG frequency band visualization (Pygame + Matplotlib)
├── run_both.py             # Launches both EEG and eye-tracking scripts in parallel
├── Prediction.ipynb        # Jupyter notebook for data analysis, feature engineering, and model training
│
├── model.pkl               # Trained ML model for EEG classification (default)
├── scaler.pkl              # Scaler for feature normalization (default)
├── ankur_signal.csv        # Example EEG data file (user-specific)
│
├── new/                    # Additional models, scalers, and signal data
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── signal.csv
│   └── new folder/
│       ├── model.pkl
│       └── scaler.pkl
│
├── esp32_1__final/         # ESP32/Arduino code and configs for EEG data acquisition
│   ├── esp32_1__final.ino  # Microcontroller firmware for reading Bioamp EXG Pill and sending serial data
│   ├── debug_custom.json
│   ├── debug.cfg
│   └── esp32.svd
│
├── signal/                 # (Empty or for future use)
│
├── .gitignore
├── README.md
└── ... (other user-specific CSVs, models, or configs)
```

---

## How It Works
1. **EEG Acquisition:**
   - The Bioamp EXG Pill captures EEG signals and outputs analog data.
   - An ESP32/Arduino digitizes this signal and streams it to the PC via serial (default: COM7, 115200 baud).
2. **Data Collection:**
   - Use `collect.py` to record EEG data for training or analysis. Data is saved as timestamped CSV files.
3. **Model Training:**
   - Use `Prediction.ipynb` to analyze collected data, extract features, and train machine learning models. Save the model as `model.pkl` and scaler as `scaler.pkl`.
4. **Real-Time Prediction:**
   - Run `prediction.py` to process live EEG data, extract features, and predict user intent. The script simulates key presses (e.g., 'space', 'w') based on predictions.
   - Optionally, run `direction.py` for webcam-based eye-tracking to control left/right actions ('a', 'd').
   - Use `run_both.py` to launch both EEG and eye-tracking controls simultaneously.
5. **Visualization:**
   - Run `visuale.py` to visualize EEG frequency bands (Delta, Theta, Alpha, Beta) in real time.

---

## Setup & Usage

### 1. **Hardware Setup**
- Connect the Bioamp EXG Pill to the subject (follow Bioamp safety guidelines).
- Connect the output to the analog input of your ESP32/Arduino.
- Upload `esp32_1__final.ino` to your microcontroller.
- Connect the microcontroller to your PC via USB.

### 2. **Software Setup**
- Install Python 3.x and required libraries (see notebook/scripts for dependencies: numpy, pandas, scipy, scikit-learn, pyautogui, pygame, matplotlib, serial, etc.).
- Adjust serial port in scripts if needed (default: COM7).

### 3. **Running the Project**
- **Collect Data:**
  ```bash
  python collect.py
  ```
- **Train Model:**
  - Use `Prediction.ipynb` to process CSV data and train a model.
- **Real-Time BCI Control:**
  ```bash
  python prediction.py
  # or
  python run_both.py  # (for EEG + eye-tracking)
  ```
- **Visualize EEG:**
  ```bash
  python visuale.py
  ```

---

## File/Folder Details
- **collect.py**: Collects EEG data from serial and saves to CSV.
- **prediction.py**: Main BCI script for real-time EEG processing and intent prediction.
- **prediction2.py**: Alternative prediction script with different features/model.
- **direction.py**: Eye-tracking for left/right gaze detection and key simulation.
- **visuale.py**: Real-time EEG frequency band visualization.
- **run_both.py**: Launches both EEG and eye-tracking scripts in parallel.
- **Prediction.ipynb**: Jupyter notebook for data analysis, feature engineering, and model training.
- **model.pkl / scaler.pkl**: Trained ML model and scaler for EEG classification.
- **esp32_1__final/**: Microcontroller code/configs for EEG data acquisition.
- **new/**: Additional models, scalers, and signal data for experiments.
- **signal/**: (Currently empty or reserved for future use.)
- **.gitignore**: Git ignore rules.
- **README.md**: This file.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgements
- [Bioamp EXG Pill](https://upsidedownlabs.tech/) for affordable, open-source biosignal hardware.
- [ESP32](https://www.espressif.com/) for microcontroller support.
- Open-source Python libraries: numpy, pandas, scipy, scikit-learn, pyautogui, pygame, matplotlib, serial, etc.

---

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. 