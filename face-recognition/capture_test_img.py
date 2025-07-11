import cv2
import os
import glob
from tqdm import tqdm
from PIL import Image
import numpy as np
import requests
from pathlib import Path
import time

Base_dir = Path(__file__).resolve().parent
ImgRootDir = f"{Base_dir}/test_images/"
# ImgRootDir = f"{Base_dir}/test_images_dk/"

def capture(name):
    dirPath = ImgRootDir + name + "/"
    if os.path.isdir(dirPath):
        pass
    else:
        os.makedirs(dirPath)

    deviceid = 0  # カメラデバイスID
    capture = cv2.VideoCapture(deviceid)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

    if not capture.isOpened():
        print("カメラのオープンに失敗しました")
        exit()

    count = 0

    while (capture.isOpened()):
        ret, frame = capture.read()
        if not ret or count >= 100:
            print("フレームの取得に失敗しました")
            break
        else:
            count += 1
            cv2.imwrite("{}{}_{}.jpg".format(dirPath, name, count), frame)
            time.sleep(0.2)

    capture.release()
    cv2.destroyAllWindows()


def main():
    print("名前を入力してください:")
    name = input()
    print("写真を撮影しています...")
    capture(name)
    print("写真の撮影が完了しました。")


if __name__ == "__main__":
    main()
