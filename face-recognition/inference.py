import cv2
from collections import Counter
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import faiss
import numpy as np
import glob
from PIL import Image

threshold = 0.7  # 類似度の閾値
ImgRootDir = "./kaggle/input/face-recognition-dataset/Original Images/Original Images/"
embedding_extensions = (".npy")

def capture():
    deviceid = 0  # カメラデバイスID
    capture = cv2.VideoCapture(deviceid)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

    if not capture.isOpened():
        print("カメラのオープンに失敗しました")
        exit()

    ret, frame = capture.read()
    if not ret:
        print("フレームの取得に失敗しました")
        exit()
    
    capture.release()
    cv2.destroyAllWindows()
    return frame

def inference(frame):
    if frame is None:
        exit()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    dim = 512# 特徴量の次元数
    nlist = 20# クラスタ数．画像数の√を目安にする？
    m = 32# PQの分類数
    nbits = 5# 量子化ビット数

    # 内積で距離を計算するためのインデックスを作成
    quantizer = faiss.IndexFlatIP(dim)
    # ベクトル検索用のインデックスを作成
    index = faiss.IndexIVFPQ(quantizer, dim, nlist, m, nbits, faiss.METRIC_INNER_PRODUCT)

    # 特徴量をロード
    embedding_files = glob.glob("./kaggle/input/face-recognition-dataset/Original Images/Original Images/*/*")
    embedding_files = [f for f in embedding_files if f.lower().endswith(embedding_extensions)]

    labels = []
    all_embeddings = []
    for file in embedding_files:
        name = file.split("/")[-2]
        data = np.load(file)
        all_embeddings.append(data)
        labels += [name] * len(data)
    
    unique_names = sorted(set(labels))
    name2id = {name: i for i, name in enumerate(unique_names)}
    id2name = {i: name for name, i in name2id.items()}

    id_labels = []
    for i in range(0, len(labels)):
        id_labels.append(name2id[labels[i]])
    
    all_embeddings = np.vstack(all_embeddings).astype('float32')
    id_labels = np.array(id_labels).astype('int64')

    # 検索のためのクラスタ構造を構築
    index.train(all_embeddings)
    # ベクトルとIDを紐付けて登録
    index.add_with_ids(all_embeddings, np.array(id_labels))

    mtcnn = MTCNN(image_size=160, margin=10, device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').to(device).eval()

    face = mtcnn(frame)
    if face is None:
        print("顔が検出できませんでした")
        exit()
    face = face.to(device)
    embedding = resnet(face.unsqueeze(0)).cpu().detach().numpy()
    D, I = index.search(embedding, 10)

    print("\n\n類似度の高い人物")
    for d, i in zip(D[0], I[0]):
        print("  distance = ", d, "index = ", i, id2name[i])

    counter = Counter(I[0])
    predicted_id, freq = counter.most_common(1)[0]
    if freq >= 5 and np.mean(D[0][:freq]) > threshold:
        print("認識された人物:", id2name[predicted_id])
    else:
        print("認識できませんでした。類似度が低いか、十分なデータがありません。")


def main():
    inference(capture())
    # inference(Image.open("test.jpg"))
    return


if __name__ == "__main__":
    main()