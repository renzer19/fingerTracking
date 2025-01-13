import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Gagal membuka kamera.")
            break

        frame = cv2.flip(frame, 1)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_tips = [4, 8, 12, 16, 20]  
                finger_base = [3, 6, 10, 14, 18]    

                count = 0
                for tip, base in zip(finger_tips, finger_base):
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
                        count += 1



                cv2.putText(frame, f"Angka: {count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        cv2.imshow('Tracking Angka dengan Tangan', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Bersihkan
cap.release()
cv2.destroyAllWindows()
