import cv2
import requests
import requests
#import pygame
import subprocess
from time import sleep
import asyncio
import switchBot
import threading
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

host = "52.43.43.101:8000"
# endpoint = f"http://{host}/face_recognition/checkin"
endpoint = f"http://{host}/estimate_pose/"

# カメラデバイスID 0 を指定
# cap = cv2.VideoCapture(0)

# カメラが開けたかチェック
#if not cap.isOpened():
    #print("エラー: カメラを開けません")
    #exit()

#pygame.init()
#pygame.mixer.init()
# 1フレーム分の画像を取得
class CameraCapture:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            print("エラー：カメラを開けません")
            exit()
        self.frame = None
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()
    
    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def get_frame(self):
        return self.frame

    def release(self):
        self.running = False
        self.cap.release()

cam = CameraCapture()
sleep(1)
while True:
    frame = cam.get_frame()

    if frame is not None:
        _, img_encoded = cv2.imencode(".jpg", frame)
        files = {"ufile" : ("img.jpg", img_encoded.tobytes(), "image/jpeg")}
        response = requests.post(url=endpoint, files = files)
        print(response.json())
        gesture = response.json().get("gesture", "unknown")
        attendance_message = response.json().get("attendance_message")
        attendance_name = response.json().get("attendance_name")
        if gesture == "hand_circle":
            print("円を認識しました")
            # aplayで音声再生（カード4のスピーカーを指定）
            try:
                subprocess.run(['aplay', '-D', 'plughw:4,0', 'pi.wav'], 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
                print("pi音声再生完了")
            except:
                print("pi音声再生に失敗しました")
            sleep(0.5)
            #sleep(4)
            #subprocess.run(["aplay", "-D", "hw:0,0", converted_wav])
            #asyncio.run(switchBot.switchBot())
            #switchBot.switchBot()
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
    else:
        print("エラー: 画像の取得に失敗しました")

    # sleep(0.1)  # 1秒待機してから次のフレームを取得
# カメラリソースを解放
cap.release()
