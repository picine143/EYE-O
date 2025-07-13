import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller, Key
import traceback
import time

running = False  # Global flag to control loop

def start_blink_detection():
    global running
    running = True

    EAR_THRESHOLD    = 0.28
    BLINK_FRAMES     = 2
    last_blink_time  = 0
    DOUBLE_BLINK_GAP = 0.7

    keyboard       = Controller()
    mp_face_mesh   = mp.solutions.face_mesh
    face_mesh      = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

    LEFT_EYE_IDX   = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_IDX  = [362, 385, 387, 263, 373, 380]
    blink_count    = 0

    def compute_EAR(pts):
        A = np.linalg.norm(pts[1] - pts[5])
        B = np.linalg.norm(pts[2] - pts[4])
        C = np.linalg.norm(pts[0] - pts[3])
        return (A + B) / (2.0 * C)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam.")
        return

    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            results = face_mesh.process(rgb)
            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0].landmark
                left_pts  = [np.array([lm[i].x, lm[i].y]) for i in LEFT_EYE_IDX]
                right_pts = [np.array([lm[i].x, lm[i].y]) for i in RIGHT_EYE_IDX]
                avgEAR = (compute_EAR(left_pts) + compute_EAR(right_pts)) / 2

                if avgEAR < EAR_THRESHOLD:
                    blink_count += 1
                else:
                    if blink_count >= BLINK_FRAMES:
                        now = time.time()
                        if now - last_blink_time <= DOUBLE_BLINK_GAP:
                            print("DOUBLE BLINK detected → SPACE")
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                            last_blink_time = 0
                        else:
                            last_blink_time = now
                    blink_count = 0
            else:
                print("No face detected.", end='\r')

        except Exception as e:
            traceback.print_exc()

        if not running:
            break

    cap.release()
    cv2.destroyAllWindows()

def stop_blink_detection(choice):
    global running
    if choice == "Single Blink":
        print("Stopping single blink detection.")
    elif choice == "Double Blink":
        print("Stopping double blink detection.")
    else:
        print("Stopping blink detection.")
        
    running = False
