import requests
import os

host = "52.43.43.101:8000"
endpoint = f"http://{host}/face_recognition/checkin"
file_path = "./ufile.jpg"

params = {}

with open(file_path, "rb") as f:
    files = {"ufile" : (file_path, f, "image/jpeg")}
    response = requests.post(url=endpoint, files = files)

print(response.json())
