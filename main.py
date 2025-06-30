import cv2
import mediapipe as mp
import math
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
last_action_time = 0
cooldown = 0.7

while cap.isOpened():
    success, frame = cap.read()
    # print(success,frame)

    if not success:
        print("Ignoring empty camera frame.")
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    # print(results.multi_hand_landmarks)
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    outer_radius = 150
    inner_radius = 40

    cv2.circle(frame, (center_x, center_y), outer_radius, (255, 255, 255), 2)
    x1 = int(center_x - outer_radius * math.cos(math.radians(45)))
    y1 = int(center_y + outer_radius * math.sin(math.radians(45)))
    x2 = int(center_x + outer_radius * math.cos(math.radians(45)))
    y2 = int(center_y - outer_radius * math.sin(math.radians(45)))
    cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
    x3 = int(center_x - outer_radius * math.cos(math.radians(45)))
    y3 = int(center_y - outer_radius * math.sin(math.radians(45)))
    x4 = int(center_x + outer_radius * math.cos(math.radians(45)))
    y4 = int(center_y + outer_radius * math.sin(math.radians(45)))
    cv2.line(frame, (x3, y3), (x4, y4), (255, 255, 255), 1)
    cv2.circle(frame, (center_x, center_y), inner_radius, (100, 100, 100), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[8]  #for index finger
            h, w, _ = frame.shape
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)
            dis=math.sqrt(math.pow(cx-center_x,2)+math.pow(cy-center_y,2))
            print(dis)
            dx = cx - center_x
            dy = center_y - cy
            angle_deg = math.degrees(math.atan2(dy, dx))
            print(angle_deg)
            current_time = time.time()
            if dis < inner_radius:
                print("IN\n")
            elif -45 <= angle_deg < 45 and current_time - last_action_time > cooldown:
                print("Right\n")
                pyautogui.press("d")
                last_action_time = current_time
            elif 45 <= angle_deg < 135 and current_time - last_action_time > cooldown:
                print("Up\n")
                pyautogui.press("w")
                last_action_time = current_time
            elif (135 <= angle_deg or angle_deg < -135) and current_time - last_action_time > cooldown:
                print("Left\n")
                pyautogui.press("a")
                last_action_time = current_time
            elif current_time - last_action_time > cooldown:
                print("Down\n")
                pyautogui.press("s")
                last_action_time = current_time

    cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()