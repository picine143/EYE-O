import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller, Key
import traceback
import time    

def start_blink_detection(isStarted):
    # ——— Configuration ———
    EAR_THRESHOLD    = 0.28    # tune this after you see EAR prints
    BLINK_FRAMES     = 2       # consecutive frames to count as a blink
    last_blink_time = 0
    DOUBLE_BLINK_GAP = 0.7

    # ——— Init ———
    keyboard       = Controller()
    mp_face_mesh   = mp.solutions.face_mesh
    face_mesh      = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
    mp_drawing     = mp.solutions.drawing_utils

    LEFT_EYE_IDX   = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_IDX  = [362, 385, 387, 263, 373, 380]
    blink_count1    = 0

    def compute_EAR(pts):
        #Calculate Euclidean distance between eye landmarks
        A = np.linalg.norm(pts[1] - pts[5]) 
        B = np.linalg.norm(pts[2] - pts[4]) 
        C = np.linalg.norm(pts[0] - pts[3])
        return (A + B) / (2.0 * C) #Formula for EAR

    # ——— Start Webcam ———
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam.")
        exit()

    #print("Webcam started. Press ESC to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("WARNING: empty frame.")
            continue

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            results = face_mesh.process(rgb)
            if results.multi_face_landmarks and isStarted:
                lm1 = results.multi_face_landmarks[0].landmark

                # get eye points
                left_pts1  = [np.array([lm1[i].x, lm1[i].y]) for i in LEFT_EYE_IDX]
                right_pts1 = [np.array([lm1[i].x, lm1[i].y]) for i in RIGHT_EYE_IDX]

                # compute EAR
                leftEAR1   = compute_EAR(left_pts1)
                rightEAR1  = compute_EAR(right_pts1)
                avgEAR1    = (leftEAR1 + rightEAR1) / 2
                #print(f"EAR: {avgEAR1:.3f}", end=' | ')


                # blink logic
                if avgEAR1 < EAR_THRESHOLD:
                    blink_count1 += 1
                else:
                    if blink_count1 >= BLINK_FRAMES:
                        now = time.time()
                        if now - last_blink_time <= DOUBLE_BLINK_GAP:
                            print("DOUBLE BLINK detected → SPACE")
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                            
                            last_blink_time = 0  # reset to avoid triple-triggering
                        else:
                            last_blink_time = now
                            # print("SINGLE BLINK")
                    blink_count1 = 0

                #draw mesh
                """ mp_drawing.draw_landmarks(
                    frame,           
                    results.multi_face_landmarks[0],
                    mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec((0,255,0),1,1)
                ) """

                
            else:
                print("No face detected.", end='\r')

        except Exception as e:
            #print("Processing error:", e)
            traceback.print_exc()

        """ cv2.imshow("Blink Test", frame) """
        if isStarted == False :  # ESC
            break      

"""     cap.release()
    cv2.destroyAllWindows()        
             """