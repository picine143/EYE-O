import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller, Key
import traceback
import time
from threading import Lock

# ——— Configuration ———
HEAD_MOVE_THRESHOLD = 15
GAZE_COOLDOWN = 0.5
EAR_THRESHOLD = 0.28
BLINK_FRAMES = 2
DOUBLE_BLINK_GAP = 0.7

# ——— Shared State ———
running = False
choice_mode = "Double Blink"
neutral_nose_pos = None
first_run = True
last_gaze_time = 0
last_blink_time = 0
blink_count = 0

should_calibrate = False
calibration_lock = Lock()

# ——— Constants ———
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

# ——— Input Interfaces ———
keyboard = Controller()


# ——— Utilities ———
def compute_EAR(pts):
    A = np.linalg.norm(pts[1] - pts[5])
    B = np.linalg.norm(pts[2] - pts[4])
    C = np.linalg.norm(pts[0] - pts[3])
    return (A + B) / (2.0 * C)

def calibrate(nose):
    return nose.copy()

def calibrate_nose():
    """External trigger for GUI to request calibration."""
    global should_calibrate
    with calibration_lock:
        should_calibrate = True


# ——— Main Detection Loop ———
def start_combined_detection(blink_mode="Double Blink", head_move_threshold= 15 , gaze_cooldown=0.5):
    global running, choice_mode, neutral_nose_pos, first_run
    global last_gaze_time, last_blink_time, blink_count
    global cap, face_mesh, should_calibrate

    HEAD_MOVE_THRESHOLD = head_move_threshold
    GAZE_COOLDOWN = gaze_cooldown

    choice_mode = blink_mode
    running = True
    first_run = True
    blink_count = 0

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam.")
        return

    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

    print("Combined detection started. Press ESC to exit, 'c' to recalibrate.")

    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]

        key = cv2.waitKey(1)

        try:
            results = face_mesh.process(rgb)
            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0].landmark

                def lm_xy(index):
                    return np.array([int(lm[index].x * w), int(lm[index].y * h)])

                nose = lm_xy(1)
                left_pts = [np.array([lm[i].x, lm[i].y]) for i in LEFT_EYE_IDX]
                right_pts = [np.array([lm[i].x, lm[i].y]) for i in RIGHT_EYE_IDX]

                # ——— Calibration ———
                with calibration_lock:
                    if first_run or key == ord('c') or should_calibrate:
                        neutral_nose_pos = calibrate(nose)
                        print(f"[Calibrated] Nose: {neutral_nose_pos}")
                        print(head_move_threshold)
                        print(gaze_cooldown)
                        should_calibrate = False
                        first_run = False

                # ——— Blink Detection ———
                avgEAR = (compute_EAR(left_pts) + compute_EAR(right_pts)) / 2
                if avgEAR < EAR_THRESHOLD:
                    blink_count += 1
                else:
                    if blink_count >= BLINK_FRAMES:
                        now = time.time()
                        if choice_mode == "Single Blink":
                            keyboard.press(Key.space); keyboard.release(Key.space)
                        elif choice_mode == "Double Blink":
                            if now - last_blink_time <= DOUBLE_BLINK_GAP:
                                keyboard.press(Key.space); keyboard.release(Key.space)
                                last_blink_time = 0
                            else:
                                last_blink_time = now
                    blink_count = 0

                # ——— Head Movement Detection ———
                dx = nose[0] - neutral_nose_pos[0]
                dy = nose[1] - neutral_nose_pos[1]
                now = time.time()

                if now - last_gaze_time > GAZE_COOLDOWN:
                    if dx < -HEAD_MOVE_THRESHOLD:
                        keyboard.press(Key.left); keyboard.release(Key.left)
                        last_gaze_time = now
                    elif dx > HEAD_MOVE_THRESHOLD:
                        keyboard.press(Key.right); keyboard.release(Key.right)
                        last_gaze_time = now
                    elif dy < -HEAD_MOVE_THRESHOLD:
                        keyboard.press(Key.up); keyboard.release(Key.up)
                        last_gaze_time = now
                    elif dy > HEAD_MOVE_THRESHOLD:
                        keyboard.press(Key.down); keyboard.release(Key.down)
                        last_gaze_time = now

        except Exception as e:
            traceback.print_exc()

       

        if key == 27:  # ESC
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Combined detection stopped.")


def stop_combined_detection():
    global running
    running = False
