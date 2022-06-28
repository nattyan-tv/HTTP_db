# HTTP_db

HTTP を使用したとっつきやすいデータベースマネージャー  
[English version](https://github.com/nattyan-tv/HTTP_db/blob/master/README.md)

# 使い方(Server)

1. Install modules (`pip install -r requirements.txt`)
2. Write `setting.json` file
3. Execute `main.py`

# 使い方(PythonClient ラッパー)

1. Install module (`pip install HTTP-db`)
2. you can use `HTTP_db` module (Please refer to `example`)

# 暗号化をする

サーバーの API リファレンスをご参照ください。

# ドキュメント

日本語ですが、API リファレンスがあります。  
[API リファレンス](https://nattyan-tv.github.io/HTTP_db/docs/index)

# 設定項目

| 名前       | 説明                                                                             | 型   |
| ---------- | -------------------------------------------------------------------------------- | ---- |
| address    | HTTP サーバーのアドレス                                                          | str  |
| port       | HTTP サーバーのポート番号                                                        | int  |
| debug      | HTTP サーバーのデバッグモード                                                    | bool |
| remotesave | リモートモード                                                                   | bool |
| location   | リモートモードが有効の場合、データベースのキー。無効の場合、データを保存する場所 | str  |
| cell       | リモートモードが有効の場合、データベースのセル。                                 | str  |
