import torch
import torch.nn as nn
import numpy as np
import joblib
import cv2
import mediapipe as mp
from sklearn.preprocessing import StandardScaler

# def extract_hand_landmarks(image, hands):
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image_rgb)
#     if results.multi_hand_landmarks:
#         landmarks = results.multi_hand_landmarks[0]
#         coords = []
#         for lm in landmarks.landmark:
#             coords.extend([lm.x, lm.y, lm.z])
#         return coords
#     return None


def extract_hand_landmarks(image, hands):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    coords = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                coords.extend([lm.x, lm.y, lm.z])
    
    if len(coords) == 63 * 2:  # 両手分（126次元）あることを確認
        return coords
    return None


def predict_hand_pose(image, model, scaler, hands):
    landmarks = extract_hand_landmarks(image, hands)
    if landmarks is None:
        return -1  # 手が検出されなかったとき

    # 特徴量の整形と標準化
    X_new = np.array(landmarks).reshape(1, -1)
    X_new_scaled = scaler.transform(X_new)
    X_tensor = torch.tensor(X_new_scaled, dtype=torch.float32)

    # 推論
    with torch.no_grad():
        output = model(X_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    return predicted_class