


# import cv2
# import dlib
# import numpy as np
# from pynput.keyboard import Controller
# from collections import deque

# # Initialize keyboard controller
# keyboard = Controller()

# # Load face detector and landmark predictor
# face_detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Ensure this file is in the same folder

# # Function to get the eye center
# def get_eye_center(eye):
#     return np.mean(eye, axis=0).astype(int)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Sensitivity settings
# MOVEMENT_THRESHOLD = 1.5  # Lower = More sensitivity
# CENTER_TOLERANCE = 3      # Increased tolerance for smoother recentring
# RESET_FRAMES = 100        # Reset center every 100 frames (adaptive)
# SMOOTHING_SIZE = 5        # Number of frames to smooth out movements

# prev_pupil_x = None
# screen_center_x = None
# key_pressed = None
# frame_count = 0
# movement_history = deque(maxlen=SMOOTHING_SIZE)  # Stores past pupil positions

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)  # Flip horizontally to correct the mirrored effect
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_detector(gray)

#     for face in faces:
#         landmarks = predictor(gray, face)
#         landmarks_points = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(68)])

#         right_eye = landmarks_points[42:48]
#         pupil_x = get_eye_center(right_eye)[0]  # Get X position of the right eye center
        
#         # Store recent positions for smoothing
#         movement_history.append(pupil_x)
#         smoothed_pupil_x = int(np.mean(movement_history))  # Apply rolling average

#         # Set screen center (dynamically resets every RESET_FRAMES)
#         if screen_center_x is None or frame_count % RESET_FRAMES == 0:
#             screen_center_x = smoothed_pupil_x
#             print("🔄 Recalibrating Center...")

#         relative_movement = smoothed_pupil_x - screen_center_x  # Difference from center

#         if relative_movement > MOVEMENT_THRESHOLD:
#             if key_pressed != 'd':
#                 keyboard.release('a')  # Release 'A'
#                 keyboard.press('d')  # Press 'D'
#                 key_pressed = 'd'
#                 print("➡️ Looking Right → Pressing 'D'")

#         elif relative_movement < -MOVEMENT_THRESHOLD:
#             if key_pressed != 'a':
#                 keyboard.release('d')  # Release 'D'
#                 keyboard.press('a')  # Press 'A'
#                 key_pressed = 'a'
#                 print("⬅️ Looking Left → Pressing 'A'")

#         elif abs(relative_movement) < CENTER_TOLERANCE:
#             if key_pressed is not None:  # Only release if a key was pressed
#                 keyboard.release('a')
#                 keyboard.release('d')
#                 key_pressed = None
#                 print("⏹️ Centered → Releasing Keys")

#     frame_count += 1  # Increment frame count
#     cv2.imshow("Eye Tracker", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# keyboard.release('a')
# keyboard.release('d')

import cv2
import mediapipe as mp
import numpy as np
import keyboard
import threading
from collections import deque


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)


MOVEMENT_THRESHOLD = 1.5  
CENTER_TOLERANCE = 10    
RESET_FRAMES = 100        
SMOOTHING_SIZE = 5        

prev_pupil_x = None
screen_center_x = None
key_pressed = None
frame_count = 0
movement_history = deque(maxlen=SMOOTHING_SIZE) 


with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
       
        frame = cv2.flip(frame, 1)
        
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
       
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
               
                right_eye_landmarks = [
                    (int(face_landmarks.landmark[33].x * frame.shape[1]), 
                     int(face_landmarks.landmark[33].y * frame.shape[0])),
                    (int(face_landmarks.landmark[133].x * frame.shape[1]), 
                     int(face_landmarks.landmark[133].y * frame.shape[0]))
                ]
                
                
                pupil_x = int(np.mean([lm[0] for lm in right_eye_landmarks]))
                
               
                movement_history.append(pupil_x)
                smoothed_pupil_x = int(np.mean(movement_history))  
                
                
                if screen_center_x is None or frame_count % RESET_FRAMES == 0:
                    screen_center_x = smoothed_pupil_x
                
                
                relative_movement = smoothed_pupil_x - screen_center_x
                
               
                if abs(relative_movement) < CENTER_TOLERANCE:
                    
                    if key_pressed is not None:
                        keyboard.release('a')
                        keyboard.release('d')
                        key_pressed = None
                elif relative_movement > MOVEMENT_THRESHOLD:
                    if key_pressed != 'd':
                        # Release 'a' if pressed
                        if keyboard.is_pressed('a'):
                            keyboard.release('a')
                        
                        # Press 'd'
                        keyboard.press('d')
                        key_pressed = 'd'
                elif relative_movement < -MOVEMENT_THRESHOLD:
                    if key_pressed != 'a':
                        # Release 'd' if pressed
                        if keyboard.is_pressed('d'):
                            keyboard.release('d')
                        
                        # Press 'a'
                        keyboard.press('a')
                        key_pressed = 'a'
                
               
                for lm in right_eye_landmarks:
                    cv2.circle(frame, lm, 3, (0, 255, 0), -1)
        
        frame_count += 1  
        
        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
