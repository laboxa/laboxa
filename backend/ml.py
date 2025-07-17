import torch.nn as nn
import mediapipe as mp
import joblib
import torch
class HandPoseClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(HandPoseClassifier, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
        )
    def forward(self, x):
        return self.model(x)
def set_up():
    mp_hands_both = mp.solutions.hands
    hands_both = mp_hands_both.Hands(static_image_mode=False, max_num_hands=2)

    scaler_both = joblib.load('scaler_all_hands.pkl')

    input_size_both = 126  # 21点×3次元×2手
    hidden_size_both = 128
    num_classes_both = 5

    model_both = HandPoseClassifier(input_size_both, hidden_size_both, num_classes_both)
    model_both.load_state_dict(torch.load("model_all_hands.pth"))
    model_both.eval()
    return model_both, scaler_both, hands_both