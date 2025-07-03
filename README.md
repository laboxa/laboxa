# LaBoXa - 音声＆ジェスチャー対応研究室アシスタント

LaBoXa は、研究室内のデバイスを音声・ジェスチャーで直感的に操作できる AI × IoT 音声アシスタント です。ユーザーのストレスを減らし、より快適で効率的な研究活動を支援します。

## 🚀 Overview

研究室における日常的な操作を自動化・簡素化し、研究者がより研究に集中できる環境を提供します。

## 🔍 Problem

研究室では以下のような課題が存在します：

- テレビや照明のリモコンやスイッチが遠く、操作が面倒
- 音声操作が周囲の雑音などで困難
- 研究室の在室状況を外部から確認できない

## 💡 Solution

LaBoXa はこれらの課題を以下の機能で解決します：

### 🎛 デバイスの一元管理
各種IoTデバイスをLaBoXa経由で集中管理・操作

### 📷 顔認証による勤怠管理
誰が在室しているかを顔認識で記録し、外部からも確認可能

### 💡 自動デバイス制御
全員が退出した場合、照明・エアコンを自動でオフに

### ✋ ジェスチャー操作対応
音声が使えない状況でも、姿勢推定で操作可能

### 🔊 音声対話システム
Google Speech Recognition で音声入力、VOICEVOX で音声出力を実現

## ✨ Features

- Centralized control of lab devices
- Facial recognition-based attendance logging
- Gesture-based control using pose estimation
- Automatic power saving (lights/AC off when everyone leaves)
- Intuitive and seamless operation, even in noisy environments

## 🛠 Tech Stack

| 技術 | 用途 |
|------|------|
| Docker | コンテナ化 |
| EC2 (AWS) | サーバー運用 |
| FastAPI | API構築 |
| Google MediaPipe | 姿勢推定・ジェスチャー認識 |
| PyTorch | モデル学習・推論 |
| CNN | 姿勢/顔認識用モデル |
| Raspberry Pi | エッジ端末 |
| Google Speech Recognition | 音声認識 |
| VOICEVOX | 音声読み上げ |

## 📦 Installation

```bash
git clone https://github.com/your-team/Laboxa.git
cd Laboxa
docker compose up
```

## 🚀 Usage

### 音声操作
```bash
"ライトをつけて"
"エアコンつけて"
"テレビをつけて"
```

### ジェスチャー操作(例)
- 手を上げる：照明ON/OFF
- 親指を上げる：エアコン温度UP
- 親指を下げる：エアコン温度DOWN