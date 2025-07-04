import numpy as np
import pygame
import matplotlib.pyplot as plt
import serial
from scipy.signal import butter, lfilter
from collections import deque


COM_PORT = "COM7"  # Change if needed
BAUD_RATE = 115200  # Match with your EEG device
    
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {COM_PORT}")
except:
    print(f"Failed to connect to {COM_PORT}")
    exit()



def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)



pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EEG Frequency Bands (COM4)")
font = pygame.font.SysFont("Arial", 24)

# Colors for different frequency bands
colors = {
    "Delta": (0, 0, 255),
    "Theta": (75, 0, 130),
    "Alpha": (0, 255, 0),
    "Beta": (255, 165, 0)
}



fs = 250  # Sample rate (Hz)
window_size = 500  # Number of points to store

# EEG data buffer
raw_data = deque([0] * window_size, maxlen=window_size)

# Buffers for each frequency band
bands = {
    "Delta": deque([0] * window_size, maxlen=window_size),
    "Theta": deque([0] * window_size, maxlen=window_size),
    "Alpha": deque([0] * window_size, maxlen=window_size),
    "Beta": deque([0] * window_size, maxlen=window_size)
}



fig, axes = plt.subplots(4, 1, figsize=(8, 6))
plt.ion()  # Interactive mode for real-time plotting



running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear screen

    
    try:
        line = ser.readline().decode("utf-8").strip()  # Read a line
        if line:
            new_sample = float(line)  # Convert to float
            raw_data.append(new_sample)
    except:
        print("Error reading data from serial.")
        continue

    
    bands["Delta"].append(bandpass_filter(list(raw_data), 0.5, 4, fs)[-1])
    bands["Theta"].append(bandpass_filter(list(raw_data), 4, 8, fs)[-1])
    bands["Alpha"].append(bandpass_filter(list(raw_data), 8, 12, fs)[-1])
    bands["Beta"].append(bandpass_filter(list(raw_data), 12, 30, fs)[-1])

    
    y_offset = 100
    for band, data in bands.items():
        pygame.draw.lines(screen, colors[band], False, 
                          [(i, HEIGHT // 2 + y_offset + int(data[i] * 3)) for i in range(len(data))], 2)
        text = font.render(f"{band} Band", True, colors[band])
        screen.blit(text, (10, y_offset))
        y_offset += 100

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

    
    for i, (band, data) in enumerate(bands.items()):
        axes[i].cla()  # Clear previous plot
        axes[i].plot(data, color=np.array(colors[band])/255.0)
        axes[i].set_title(f"{band} Band")
        axes[i].set_ylim(-20, 20)

    plt.pause(0.01)

pygame.quit()
ser.close()
plt.ioff()
plt.show()






