# HTTP_db
HTTPを使用したとっつきやすいデータベースマネージャー  
[English version](https://github.com/nattyan-tv/HTTP_db/blob/master/README.md)

# 使い方
1. 必要なモジュールをインストールします (`pip install -r requirements.txt`)
2. `setting.json`に必要な項目を書き込みます
3. `main.py`を実行します

# API Reference
[こちら（日本語版）](https://nattyan-tv.github.io/HTTP_db/docs/ja-jp/index)  
[こちら（英語版）](https://nattyan-tv.github.io/HTTP_db/docs/en-us/index)  

# 設定項目
名前|説明|型
---|---|---
address|HTTPサーバーのアドレス|str
port|HTTPサーバーのポート番号|int
debug|HTTPサーバーのデバッグモード|bool
filename|データベースのファイル名|str
