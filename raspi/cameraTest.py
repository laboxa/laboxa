import cv2
import requests

host = "52.43.43.101:8000"
# endpoint = f"http://{host}/face_recognition/checkin"
endpoint = f"http://{host}/estimate_pose/"

# カメラデバイスID 0 を指定
cap = cv2.VideoCapture(0)

# カメラが開けたかチェック
if not cap.isOpened():
    print("エラー: カメラを開けません")
    exit()

# 1フレーム分の画像を取得
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
else:
    print("エラー: 画像の取得に失敗しました")

# カメラリソースを解放
cap.release()
