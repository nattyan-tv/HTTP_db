# HTTP_db

HTTP を使用したとっつきやすいデータベースマネージャー  
[English version](https://github.com/nattyan-tv/HTTP_db/blob/master/README.md)

# 使い方

1. 必要なモジュールをインストールします (`pip install -r requirements.txt`)
2. `setting.json`に必要な項目を書き込みます
3. `main.py`を実行します

# ドキュメント

API リファレンスがあります。  
[日本語](https://nattyan-tv.github.io/HTTP_db/docs/ja-jp/index)  
[英語](https://nattyan-tv.github.io/HTTP_db/docs/en-us/index)

# 設定項目

| 名前       | 説明                                                                             | 型   |
| ---------- | -------------------------------------------------------------------------------- | ---- |
| address    | HTTP サーバーのアドレス                                                          | str  |
| port       | HTTP サーバーのポート番号                                                        | int  |
| debug      | HTTP サーバーのデバッグモード                                                    | bool |
| remotesave | リモートモード                                                                   | bool |
| location   | リモートモードが有効の場合、データベースのキー。無効の場合、データを保存する場所 | str  |
| cell       | リモートモードが有効の場合、データベースのセル。                                 | str  |
