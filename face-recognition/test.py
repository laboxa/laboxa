from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np
import faiss
import torch
import glob
from tqdm import tqdm

image_extensions = (".jpg")
files = glob.glob("./kaggle/input/face-recognition-dataset/Original Images/Original Images/*/*")
files = [f for f in files if f.lower().endswith(image_extensions)]

# 名前を取得
labels = []
for file in files:
    name = file.split("/")[-2]
    labels.append(name)



unique_names = sorted(set(labels))
name2id = {name: i for i, name in enumerate(unique_names)}
id2name = {i: name for name, i in name2id.items()}

print(id2name)

# trainとtestに分割
train_files, train_labels = [],[]
for i in range(0, len(files), 2):
    train_files.append(files[i])
    train_labels.append(name2id[labels[i]])

test_files, test_labels = [], []
for i in range(1, len(files), 2):
    test_files.append(files[i])
    test_labels.append(name2id[labels[i]])


# facenet, faissの初期化
device = "cuda" if torch.cuda.is_available() else "cpu"

dim = 512# 特徴量の次元数
nlist = 20# クラスタ数．画像数の√を目安にする？
m = 32# PQの分類数
nbits = 5# 量子化ビット数

# 内積で距離を計算するためのインデックスを作成
quantizer = faiss.IndexFlatIP(dim)
# ベクトル検索用のインデックスを作成
index = faiss.IndexIVFPQ(quantizer, dim, nlist, m, nbits, faiss.METRIC_INNER_PRODUCT)


# 顔検出と特徴抽出のためのモデルを初期化
mtcnn = MTCNN(image_size=160, margin=10, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').to(device).eval()



# 顔画像の特徴量を抽出
embeddings = None
for file in tqdm(train_files):
    img = Image.open(file)
    img = mtcnn(img).to(device)
    embedding = resnet(img.unsqueeze(0)).cpu().detach().numpy()
    if embeddings is None:
        embeddings = embedding
    else:
        embeddings = np.concatenate((embeddings, embedding), axis=0)


# 検索のためのクラスタ構造を構築
index.train(embeddings)
# ベクトルとIDを紐付けて登録
index.add_with_ids(embeddings, np.array(train_labels))




# 1:N 検索を実行
# top-10 accuracy

for i, (label, file) in enumerate(zip(test_labels, test_files)) :
    if i%50 == 0 :
        img = Image.open(file)
        img = mtcnn(img).to(device)
        embedding = resnet(img.unsqueeze(0)).cpu().detach().numpy()
        D, I = index.search(embedding, 10) 
        print("label=", label, id2name[label])
        for d, i in zip(D[0], I[0]):
            if label == i :
                print("  distance = ", d, "guess = ", id2name[i], "answer = ", id2name[label], "---OK")
            else:
                print("  distance = ", d, "guess = ", id2name[i], "answer = ", id2name[label], "xxxNG")





"""
# 以下はカメラから人を判断するコードの例です
# ただし，実行環境によってはカメラが利用できない場合があります
"""
import cv2
from collections import Counter

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





threshold = 0.7  # 類似度の閾値


img = mtcnn(frame).to(device)
embedding = resnet(img.unsqueeze(0)).cpu().detach().numpy()
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

