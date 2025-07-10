FROM python:3.8.10

# 必要なツール（Rust含む）をインストール
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /workdir
COPY ./requirements.txt /workdir/

RUN apt-get install -y portaudio19-dev && \
    pip install pyaudio

RUN pip install --upgrade pip \
    && pip install -r /workdir/requirements.txt
