# hand_circle.py
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,  # 静止画モード
    max_num_hands=2,
    min_detection_confidence=0.5
)

def calc_distance(lm1, lm2):
    return math.hypot(lm1.x - lm2.x, lm1.y - lm2.y)

def calc_angle(p1, p2, p3):
    a = [p1.x - p2.x, p1.y - p2.y]
    b = [p3.x - p2.x, p3.y - p2.y]
    dot = a[0]*b[0] + a[1]*b[1]
    norm_a = math.hypot(*a)
    norm_b = math.hypot(*b)
    if norm_a * norm_b == 0:
        return 0
    angle_rad = math.acos(min(1, max(-1, dot / (norm_a * norm_b))))
    return math.degrees(angle_rad)

def is_finger_up(lm, tip_id, pip_id): return lm.landmark[tip_id].y < lm.landmark[pip_id].y
def is_thumb_up(lm): return abs(lm.landmark[4].x - lm.landmark[2].x) > 0.1 and lm.landmark[4].y < lm.landmark[3].y
def is_peace_sign(lm): return is_finger_up(lm, 8, 6) and is_finger_up(lm, 12, 10) and not is_finger_up(lm, 16, 14) and not is_finger_up(lm, 20, 18)
def is_index_and_pinky_up_only(lm): return is_finger_up(lm, 8, 6) and is_finger_up(lm, 20, 18) and not is_thumb_up(lm) and not is_finger_up(lm, 12, 10) and not is_finger_up(lm, 16, 14)
def is_thumb_index_right_angle_with_fist(lm):
    angle = calc_angle(lm.landmark[4], lm.landmark[2], lm.landmark[8])
    return (40 <= angle <= 150) and not is_finger_up(lm, 12, 10) and not is_finger_up(lm, 16, 14) and not is_finger_up(lm, 20, 18)
def is_both_hands_circle(h1, h2): return calc_distance(h1.landmark[8], h2.landmark[8]) < 0.3 and calc_distance(h1.landmark[4], h2.landmark[4]) < 0.3

# この関数を main.py から呼び出す
def detect_hand_gesture(image_bgr, check_fingers):
    image_rgb = image_bgr[:, :, ::-1]
    results = hands.process(image_rgb)

    if not results.multi_hand_landmarks:
        return "no_gesture"

    hands_list = results.multi_hand_landmarks

    if len(hands_list) == 2:
        if is_both_hands_circle(hands_list[0], hands_list[1]) and not check_fingers:
            return "hand_circle"

    if check_fingers:
        for lm in hands_list:
            if is_peace_sign(lm):
                return "piece"
            elif is_index_and_pinky_up_only(lm):
                return "corna"
            elif is_thumb_index_right_angle_with_fist(lm):
                return "vertical"

    return "no_gesture"
