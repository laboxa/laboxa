import cv2
from collections import Counter
import os

name = 'kazuya IKEUCHI'
dirPath = './kaggle/input/face-recognition-dataset/Original Images/Original Images/' + name + '/'
if os.path.isdir(dirPath):
    pass
else:
    os.makedirs(dirPath)

deviceid = 0  # カメラデバイスID
capture = cv2.VideoCapture(deviceid)

if not capture.isOpened():
    print("カメラのオープンに失敗しました")
    exit()

count = 0

while (capture.isOpened()):
    ret, frame = capture.read()
    if not ret or count >= 50:
        print("フレームの取得に失敗しました")
        break
    else:
        count += 1
        cv2.imwrite("{}{}_{}.jpg".format(dirPath, name, count), frame)

capture.release()
cv2.destroyAllWindows()