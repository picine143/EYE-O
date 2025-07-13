import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller, Key
import traceback
import time


def start():
    HEAD_MOVE_THRESHOLD =   15    # pixels of nose movement to register direction
    GAZE_COOLDOWN       = 0.1     # seconds between head gesture detections
    neutral_nose_pos = None
    first_run = True


    # ——— Init ———
    keyboard         = Controller()
    face_mesh        = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
    mp_drawing       = mp.solutions.drawing_utils
    LEFT_EYE_IDX     = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_IDX    = [362, 385, 387, 263, 373, 380]


    def calibrate(nose):
        return nose.copy()

    last_gaze_time   = 0

    def compute_EAR(pts):
        A = np.linalg.norm(pts[1] - pts[5])
        B = np.linalg.norm(pts[2] - pts[4])
        C = np.linalg.norm(pts[0] - pts[3])
        return (A + B) / (2.0 * C)

    # ——— Webcam ———
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam.")
        exit()

    print("Running... Press ESC to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("WARNING: empty frame.")
            continue

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w  = frame.shape[:2]

        key = cv2.waitKey(1)

        try:
            results = face_mesh.process(rgb)
            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0].landmark

                # ——— Helper: convert to pixel coordinates ———
                def lm_xy(index):
                    return np.array([int(lm[index].x * w), int(lm[index].y * h)])

            

            
                
                # ——— Head Movement Detection ———
                nose = lm_xy(1)  # landmark 1 is nose tip

                if first_run:
                    neutral_nose_pos = calibrate(nose)
                    print(f"[Auto] Calibrated nose at: {neutral_nose_pos}")
                    first_run = False

                if key == ord('c'):
                    neutral_nose_pos = nose.copy()
                    print(f"[Manual] Calibrated nose at: {neutral_nose_pos}")

                
                dx = nose[0] - neutral_nose_pos[0]
                dy = nose[1] - neutral_nose_pos[1]
                now = time.time()

                if now - last_gaze_time > GAZE_COOLDOWN:
                    if dx < -HEAD_MOVE_THRESHOLD:
                        print("LEFT")
                        keyboard.press(Key.left); keyboard.release(Key.left)
                        last_gaze_time = now
                    elif dx > HEAD_MOVE_THRESHOLD:
                        print("RIGHT")
                        keyboard.press(Key.right); keyboard.release(Key.right)
                        last_gaze_time = now
                    elif dy < -HEAD_MOVE_THRESHOLD:
                        print("UP")
                        keyboard.press(Key.up); keyboard.release(Key.up)
                        last_gaze_time = now
                    elif dy > HEAD_MOVE_THRESHOLD:
                        print("DOWN")
                        keyboard.press(Key.down); keyboard.release(Key.down)
                        last_gaze_time = now

            

        except Exception as e:
            traceback.print_exc()

        # ——— Draw camera ———   
        cv2.putText(frame, "Press 'c' to calibrate nose position", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press ESC to exit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("Head Movement Detection", frame)

    
        if key == 27:  # ESC
            print("ESC pressed. Exiting.")
            break

