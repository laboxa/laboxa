import requests
import glob
import os

ImgRootDir = "./kaggle/input/face-recognition-dataset/Original Images/Original Images/"
embedding_extensions = (".npy")

embedding_files = glob.glob("./kaggle/input/face-recognition-dataset/Original Images/Original Images/*/*")
embedding_files = [f for f in embedding_files if f.lower().endswith(embedding_extensions)]

host = "52.43.43.101:8000"
endpoint = f"http://{host}/face_recognition/upload_npy"
# headers = {
#     "Content-Type": "multipart/form-data",
# }
for file in embeding_files:
    name = file.split("/")[-2]
    params = {
        "name": name,
    }
    with open(file, "rb") as f:
        files = {"npy_file": (os.path.basename(file_path), f, "application/octet-stream")}

    response = request.post(url=endpoint, data=params, files = files)
    print(response.json())
