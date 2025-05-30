# Face Recognition API

## 概要

### 提供機能
- ユーザ登録・削除
- 入退室管理


## API
### ユーザ登録・削除
|             |メソッド|URL|
|:-:|:-:|:-:|
|ユーザを登録する|POST|/users/registration|
|ユーザを削除する|POST|/users/delete|
|顔情報の更新   |POST|/users/update|

### 入退室管理
|           |メソッド|URL         |
|:---------:|:-----:|:---------:|
|入室する     |POST  |/api/enter  |
|退室する     |POST  |/api/exit   |
|在室状況を取得|GET   |/api/entries|
