import cv2
import mediapipe as mp
import socket
import numpy as np
import time

# ================= UDP CONFIG =================
ESP_IP = "192.168.4.1"
ESP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_servo(id, angle):
    angle = int(np.clip(angle, 0, 180))
    msg = f"S{id}:{angle}"
    sock.sendto(msg.encode(), (ESP_IP, ESP_PORT))

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

print("Hand Control Started - Press Q to quit")

gripper_state = None  # prevents spamming UDP

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark

        # ================= BASE =================
        base_angle = np.interp(lm[0].x, [0.0, 1.0], [0, 180])
        send_servo(0, base_angle)

        # ================= SHOULDER =================
        shoulder_angle = np.interp(lm[0].y, [0.0, 1.0], [0, 180])
        send_servo(1, shoulder_angle)

        # ================= FINGER STATE DETECTION =================
        fingers_open = 0

        # Thumb (x comparison because thumb moves sideways)
        if lm[4].x > lm[3].x:
            fingers_open += 1

        # Index
        if lm[8].y < lm[6].y:
            fingers_open += 1

        # Middle
        if lm[12].y < lm[10].y:
            fingers_open += 1

        # Ring
        if lm[16].y < lm[14].y:
            fingers_open += 1

        # Pinky
        if lm[20].y < lm[18].y:
            fingers_open += 1

        # ================= GRIPPER LOGIC =================
        if fingers_open >= 4:
            if gripper_state != "open":
                send_servo(5, 90)
                print("Gripper OPEN")
                gripper_state = "open"

        elif fingers_open <= 1:
            if gripper_state != "close":
                send_servo(5, 0)
                print("Gripper CLOSE")
                gripper_state = "close"

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()
