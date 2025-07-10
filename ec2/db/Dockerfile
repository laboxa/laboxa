# MySQL 8.0ベースイメージを使用
FROM mysql:8.0

# 文字セット設定のための設定ファイルをコピー
COPY my.cnf /etc/mysql/conf.d/

# 初期化SQLファイルをコピー
COPY init.sql /docker-entrypoint-initdb.d/

# ポート3306を公開
EXPOSE 3306