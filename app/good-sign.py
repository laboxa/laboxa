import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def vector_angle(v1, v2):
    """2つのベクトルのなす角を計算（ラジアン→度）"""
    dot = sum(a*b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(b*b for b in v2))
    if mag1 * mag2 == 0:
        return 180
    return math.degrees(math.acos(dot / (mag1 * mag2)))

def is_thumb_up(landmarks):
    # 親指の方向ベクトル
    thumb_vec = [
        landmarks[4].x - landmarks[2].x,
        landmarks[4].y - landmarks[2].y,
        landmarks[4].z - landmarks[2].z,
    ]
    # 手首から中指方向（上方向）
    up_vec = [
        landmarks[9].x - landmarks[0].x,
        landmarks[9].y - landmarks[0].y,
        landmarks[9].z - landmarks[0].z,
    ]
    angle = vector_angle(thumb_vec, up_vec)
    return angle < 30  # ← 親指が「上方向」に向いていると判定

def is_good_sign(landmarks):
    thumb_ok = is_thumb_up(landmarks)

    fingers_folded = all(
        landmarks[tip].y > landmarks[tip - 2].y - 0.02
        for tip in [8, 12, 16, 20]
    )

    return thumb_ok and fingers_folded

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=5,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if is_good_sign(hand_landmarks.landmark):
                    cv2.putText(image, 'Good Sign 👍', (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                else:
                    cv2.putText(image, 'Not Good', (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        cv2.imshow('Good Sign Detection', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()

