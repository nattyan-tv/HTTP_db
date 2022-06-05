# HTTP_db
Simple and easy database manager using HTTP  
[日本語版](https://github.com/nattyan-tv/HTTP_db/blob/master/README_ja.md)

# Usage
1. Install modules (`pip install -r requirements.txt`)
2. Write `setting.json` file
3. Execute `main.py`

# API Reference
[English version](https://nattyan-tv.github.io/HTTP_db/docs/en-us/index)  
[Japanese version](https://nattyan-tv.github.io/HTTP_db/docs/ja-jp/index)  

# Setting

Name|Description|Type
---|---|---
address|HTTP Server address|str
port|HTTP Server port|int
debug|HTTP Server debug mode|bool
remotesave|Remote save mode|bool
location|If remotesave is true, database key, else, savedata location|str
cell|If remotesave is true, database cell|str
