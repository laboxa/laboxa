import cv2
import requests
import subprocess
import asyncio
import threading
from time import sleep
from config import API_HOST, CAMERA_DEVICE, SPEAKER_DEVICE
import switchBot
import zunda

# text = "あああ"
# # Step 1: 音声合成クエリ
# params = {
#     "text": text,
#     "speaker": 1
# }
# resp = requests.post("http://localhost:50021/audio_query", params=params)
# audio_query = resp.json()
# 
# # Step 2: 音声合成
# resp = requests.post("http://localhost:50021/synthesis?speaker=1", json=audio_query)
# wavfile = f"output.wav"
# with open(wavfile, "wb") as f:
#     f.write(resp.content)
# 
# # Step 3: soxで48kHz stereoに変換
# converted_wav = f"output_48k_stereo.wav"
# subprocess.run(["sox", wavfile, "-r", "48000", "-c", "2", converted_wav])

# APIエンドポイント
endpoint = f"http://{API_HOST}/estimate_pose_ml/"

class CameraCapture:
    """カメラ映像をバックグラウンドで取得するクラス"""
    def __init__(self, src=CAMERA_DEVICE):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            print("エラー：カメラを開けません")
            exit()
        self.frame = None
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()
    
    def update(self):
        """フレームを継続的に更新"""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def get_frame(self):
        return self.frame

    def release(self):
        self.running = False
        self.cap.release()

def play_sound(sound_file):
    """音声ファイルを再生"""
    try:
        subprocess.run(['aplay', '-D', SPEAKER_DEVICE, sound_file], 
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"音声再生エラー: {e}")

def process_gesture(gesture, attendance_message, attendance_name):
    """ジェスチャーに応じた処理を実行"""
    if gesture == "hand_circle":
        print("円を認識しました")
        play_sound('pi.wav')
        sleep(0.5)
    elif gesture == 'piece':
        if attendance_message == 'checkin':
            print(f"{attendance_name}さんが入室しました")
            zunda.talk(f"{attendance_name}さんが入室しました")
        else:
            print("入室できませんでした")
            zunda.talk("入室できませんでした")
    elif gesture == 'corna':
        if attendance_message == 'checkout':
            print(f"{attendance_name}さんが退室しました")
            zunda.talk(f"{attendance_name}さんが退室しました")
        else:
            print("退室できませんでした")
            zunda.talk("退室できませんでした")
    elif gesture == 'vertical':
        asyncio.run(switchBot.switchBot()) 
        print("スイッチを操作しました")
        zunda.talk("スイッチを操作しました")
    elif gesture == 'no_gesture':
        print("ジェスチャーが認識されませんでした")

def main():
    """メイン処理"""
    cam = CameraCapture()
    sleep(1)
    
    while True:
        frame = cam.get_frame()
        
        if frame is not None:
            _, img_encoded = cv2.imencode(".jpg", frame)
            files = {"ufile": ("img.jpg", img_encoded.tobytes(), "image/jpeg")}
            
            try:
                response = requests.post(url=endpoint, files=files)
                response_data = response.json()
                print(response_data)
                
                gesture = response_data.get("gesture", "unknown")
                attendance_message = response_data.get("attendance_message")
                attendance_name = response_data.get("attendance_name")
                
                process_gesture(gesture, attendance_message, attendance_name)
                
            except Exception as e:
                print(f"API通信エラー: {e}")
        else:
            print("エラー: 画像の取得に失敗しました")

if __name__ == "__main__":
    main()
