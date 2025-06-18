# バックエンドAPI

## 主なAPIエンドポイント
### 顔認識
|メソッド|データ形式|URL                         |説明           |
|:-----:|:-------:|:--------------------------:|:-------------:|
|POST   |form-data|/face_recognition/inference |顔の推定        |
|POST   |form-data|/face_recognition/upload_npy|npyファイル登録 |