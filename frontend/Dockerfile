# Node.js 18のAlpineイメージを使用
FROM node:18-alpine

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonをコピー
COPY package.json ./

# 依存関係をインストール
RUN npm install --legacy-peer-deps

# アプリケーションのソースコードをコピー
COPY . .

# ポート3000を公開
EXPOSE 3000

# 開発サーバーを起動
CMD ["npm", "run", "dev"]