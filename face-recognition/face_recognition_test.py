from collections import Counter
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import faiss
import numpy as np
import glob
from pathlib import Path
import os
import cv2
from PIL import Image
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix

Base_dir = Path(__file__).resolve().parent
Embedding_extensions = (".npy")


class Face_recognition:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # パラメータ
    threshold = 0.5  # 類似度の閾値
    dim = 512# 特徴量の次元数
    nlist = 20# クラスタ数．画像数の√を目安にする？
    m = 32# PQの分類数
    nbits = 5# 量子化ビット数

    # ベクトル検索
    index = None

    # データ
    name2id = None
    id2name = None

    # 顔検出・特徴量抽出
    mtcnn = None
    resnet = None
    
    def __init__(self):
        quantizer = faiss.IndexFlatIP(self.dim)
        self.index = faiss.IndexIVFPQ(quantizer, self.dim, self.nlist, self.m, self.nbits, faiss.METRIC_INNER_PRODUCT)

        self.update()

        self.mtcnn = MTCNN(image_size=160, margin=10, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').to(self.device).eval()
    
    def update(self):
        embedding_files = glob.glob(f"{Base_dir}/kaggle/input/face-recognition-dataset/Original Images/Original Images/*/*")
        embedding_files = [f for f in embedding_files if f.lower().endswith(Embedding_extensions)]

        labels = []
        id_labels = []
        all_embeddings = []
        for file in embedding_files:
            name = file.split("/")[-2]
            data = np.load(file)
            all_embeddings.append(data)
            labels += [name] * len(data)
        
        unique_names = sorted(set(labels))
        name2id = None
        id2name = None
        self.name2id = {name: i for i, name in enumerate(unique_names)}
        self.id2name = {i: name for name, i in self.name2id.items()}
        
        for i in range(0, len(labels)):
            id_labels.append(self.name2id[labels[i]])
        
        if all_embeddings == []:
            return
        
        all_embeddings = np.vstack(all_embeddings).astype('float32')
        id_labels = np.array(id_labels).astype('int64')

        self.index.train(all_embeddings)
        # ベクトルとIDを紐付けて登録
        self.index.add_with_ids(all_embeddings, np.array(id_labels))
        
    def inference(self, frame):
        if frame is None:
            exit()
        face = self.mtcnn(frame)
        if face is None:
            print("顔が検出できませんでした")
            return {"status": "no_face", "name": None}
        face = face.to(self.device)
        embedding = self.resnet(face.unsqueeze(0)).cpu().detach().numpy()
        D, I = self.index.search(embedding, 10)

        # print("\n\n類似度の高い人物")
        # for d, i in zip(D[0], I[0]):
            # print("  distance = ", d, "index = ", i, self.id2name[i])

        counter = Counter(I[0])
        predicted_id, freq = counter.most_common(1)[0]
        # if freq >= 5 and np.mean(D[0][:freq]) > self.threshold:
        if np.mean(D[0][0]) > self.threshold:
            # print("認識された人物:", self.id2name[predicted_id])
            return {"status": "true", "name": self.id2name[predicted_id]}
        else:
            print("認識できませんでした")
            return {"status": "unknown", "name": None}

recognizer = Face_recognition()

test_root = f"{Base_dir}/test_images/"

y_true = []
y_pred = []

for person_name in os.listdir(test_root):
    print(person_name)
    person_dir = os.path.join(test_root, person_name)
    if not os.path.isdir(person_dir):
        continue

    for img_file in tqdm(os.listdir(person_dir)):
        if not img_file.lower().endswith(".jpg"):
            continue

        img_path = os.path.join(person_dir, img_file)
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_rgb)

        result = recognizer.inference(pil_image)

        if result["status"] == "no_face":
            continue
        elif result["status"] == "true":
            y_true.append(person_name)
            y_pred.append(result["name"])
        else:
            y_true.append(person_name)
            y_pred.append("unknown")

# 精度評価

print("\n結果")
print("正解ラベル:", y_true)
print("予測ラベル:", y_pred)

print("\n精度評価:")
print(classification_report(y_true, y_pred, zero_division=0))

print("\n混同行列:")
labels = sorted(set(y_true + y_pred))
print(confusion_matrix(y_true, y_pred, labels=labels))

