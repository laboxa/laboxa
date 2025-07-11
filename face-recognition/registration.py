import cv2
import os
import glob
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from tqdm import tqdm
from PIL import Image
import numpy as np
import requests
import os
import time

ImgRootDir = "./kaggle/input/face-recognition-dataset/Original Images/Original Images/"
image_extensions = (".jpg")
embedding_extensions = (".npy")

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
            time.sleep(0.2)  # 少し待つことでカメラのフレームレートに対応

    capture.release()
    cv2.destroyAllWindows()

def learn(name):
    files = glob.glob(ImgRootDir + name + "/*")
    files = [f for f in files if f.lower().endswith(image_extensions)]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    # 顔検出と特徴抽出のためのモデルを初期化
    mtcnn = MTCNN(image_size=160, margin=10, device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').to(device).eval()

    embeddings = []
    for file in tqdm(files):
        img = Image.open(file)
        face = mtcnn(img)
        if face is None:
            print("顔が検出できませんでした: {file}")
            continue
        face = face.to(device)
        embedding = resnet(face.unsqueeze(0)).cpu().detach().numpy()
        embeddings.append(embedding[0])
    
    if len(embeddings) == 0:
        print("有効な特徴量が取得できませんでした")
        exit()
    
    embeddings = np.stack(embeddings)

    np.save(f"{ImgRootDir}{name}/{name}_all_embeddings.npy", embeddings)

host = "52.43.43.101:8000"
endpoint = f"http://{host}/face_recognition/upload_npy"

def send(name):
    embedding_files = glob.glob(f"./kaggle/input/face-recognition-dataset/Original Images/Original Images/{name}/*")
    embedding_files = [f for f in embedding_files if f.lower().endswith(embedding_extensions)]
    for file in embedding_files:
        params = {
            "name": name,
        }
        with open(file, "rb") as f:
            files = {"npy_file": (f"{name}_all_embeddings.npy", f, "application/octet-stream")}
            response = requests.post(url=endpoint, data=params, files = files)
            print(response.json())
        break


def main():
    print("名前を入力してください")
    name = input()
    print("写真を撮影しています．カメラに注目してください")
    capture(name)
    print("撮影が終了しました")
    print("特徴量を抽出します")
    learn(name)
    print("特徴量を抽出しました")
    # send(name)
    # print ("特徴量を送信しました")


if __name__ == "__main__":
    main()