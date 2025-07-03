# Python 3.11のAlpineイメージを使用
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libmariadb-dev-compat

# requirements.txtをコピー
COPY requirements.txt .

# Python依存関係をインストール
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
# COPY . .

# ポート8000を公開
EXPOSE 8000

# FastAPIアプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]