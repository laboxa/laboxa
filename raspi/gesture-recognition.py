import cv2
import requests
import requests
import pygame
import subprocess
from time import sleep
import asyncio
import switchBot

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
cap = cv2.VideoCapture(0)

# カメラが開けたかチェック
if not cap.isOpened():
    print("エラー: カメラを開けません")
    exit()

pygame.mixer.init()
# 1フレーム分の画像を取得
while True:
    ret, frame = cap.read()

    if ret:
        # 取得した画像を保存
        filename = "captured_image.jpg"
        cv2.imwrite(filename, frame)
        print(f"画像を保存しました: {filename}")
        # send
        _, img_encoded = cv2.imencode(".jpg", frame)
        files = {"ufile" : ("img.jpg", img_encoded.tobytes(), "image/jpeg")}
        response = requests.post(url=endpoint, files = files)
        print(response.json())
        gesture = response.json().get("gesture", "unknown")
        if gesture == "hand_circle":
            print("円を認識しました")
            activation_sound = pygame.mixer.Sound("pi.wav")
            activation_sound.play()
            sleep(4)
            #subprocess.run(["aplay", "-D", "hw:0,0", converted_wav])
            asyncio.run(switchBot.switchBot())
            #switchBot.switchBot()
    elif gesture == 'no_gesture':
            print("ジェスチャーが認識されませんでした")
    else:
        print("エラー: 画像の取得に失敗しました")

    #sleep(1)  # 1秒待機してから次のフレームを取得
# カメラリソースを解放
cap.release()