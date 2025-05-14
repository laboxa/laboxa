FROM python:3.10-slim

# OSパッケージのインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean
# 作業ディレクトリ
WORKDIR /app

# 必要なPythonパッケージ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY app/ .

#CMD ["python", "main.py"]
CMD ["python", "good-sign.py"]
