# インフォ

`HTTP_db`は、HTTP を使用してデータの書き込みや読み込みを行う、簡易的かつとっつき易い、データベースマネージャーです。

# 使い方

`Client`インスタンスを初期化します。  
その初期化したインスタンスで関数を実行することでデータ取得などがおこなえます。

```py
clinet = HTTP_db.Clinet(urL="localhost", port=8080, password="amagasaki2022")

datas = await client.get_all()
await client.post("temp", datas)
```

# API リファレンス

## Client

`class HTTP_db.Client(url, port, password)`

- 関数:
  - async [`info`](#await-info)
  - async [`get`](#await-get)
  - async [`get_all`](#await-getall)
  - async [`post`](#await-post)
  - async [`delete`](#await-delete)
  - async [`delete_all`](#await-deleteall)
- 引数:
  - `url` ([str](https://docs.python.org/3/library/functions.html#func-str)): サーバーアドレス
  - `port` ([int](https://docs.python.org/3/library/functions.html#int)): サーバーポート
  - `password` ([str](https://docs.python.org/3/library/functions.html#func-str)): データベースのパスワードです。パスワードをかけていない場合は不要です。

### 関数

### _await_ **info()**

この関数は[_コルーチン_](https://docs.python.org/3/library/asyncio-task.html#coroutine)です。  
サーバーに関する情報を含む[_dict_](https://docs.python.org/3/library/stdtypes.html#dict)を返します。

- 引数:
  - None
- 返り値:
  - [_dict_](https://docs.python.org/3/library/stdtypes.html#dict)

### _await_ **get(_key_)**

この関数は[_コルーチン_](https://docs.python.org/3/library/asyncio-task.html#coroutine)です。  
指定されたキーのデータを含む[_dict_](https://docs.python.org/3/library/stdtypes.html#dict)を返します。

- 引数:
  - `key` ([str](https://docs.python.org/3/library/functions.html#func-str)): データのキー
- 例外:
  - [**`DatabaseKeyError`**](#exception-databasekeyerror) - キーが存在しなかった場合
  - [**`DatabaseReadError`**](#exception-databasereaderror) - サーバー側で読み込みエラーが発生した場合
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - サーバーとの接続などでエラーが発生した場合
- 返り値:
  - [_dict_](https://docs.python.org/3/library/stdtypes.html#dict)

### _await_ **get_all()**

この関数は[_コルーチン_](https://docs.python.org/3/library/asyncio-task.html#coroutine)です。  
データベースに格納されているすべてのデータを含む[_dict_](https://docs.python.org/3/library/stdtypes.html#dict)を返します。

- 引数:
  - なし
- 例外:
  - [**`DatabaseReadError`**](#exception-databasereaderror) - サーバー側で読み込みエラーが発生した場合
- 返り値:
  - [_dict_](https://docs.python.org/3/library/stdtypes.html#dict)

### _await_ **post(_key_, _data_)**

この関数は[_コルーチン_](https://docs.python.org/3/library/asyncio-task.html#coroutine)です。  
指定されたキーにデータを格納します。

- 引数:
  - `key` ([str](https://docs.python.org/3/library/functions.html#func-str)): データのキー
  - `data` ([_dict_](https://docs.python.org/3/library/stdtypes.html#dict)): データの値
- 例外:
  - [**`DatabaseWriteError`**](#exception-databasewriteerror) - サーバー側で書き込みエラーが発生した場合
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - サーバーとの接続などでエラーが発生した場合
- 返り値:
  - なし

### _await_ **delete(_key_)**

この関数は[_コルーチン_](https://docs.python.org/3/library/asyncio-task.html#coroutine)です。  
指定されたキーに格納されているデータを削除します。

- 引数:
  - `key` ([str](https://docs.python.org/3/library/functions.html#func-str)): データのキー
- 例外:
  - [**`DatabaseKeyError`**](#exception-databasekeyerror) - キーが存在しなかった場合
  - [**`DatabaseDeleteError`**](#exception-databasedeleteerror) - サーバー側で削除エラーが発生した場合
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - サーバーとの接続などでエラーが発生した場合
- 返り値:
  - なし

### _await_ **delete_all()**

この関数は[_コルーチン_](https://docs.python.org/3/library/asyncio-task.html#coroutine)です。  
データベースに格納されているすべてのデータを削除します。

- 引数:
  - なし
- 例外:
  - [**`DatabaseDeleteError`**](#exception-databasedeleteerror) - サーバー側で削除エラーが発生した場合
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - サーバーとの接続などでエラーが発生した場合
- 返り値:
  - なし

## Ping

`class HTTP_db.Ping()`

- Attributes:
  - [`send`](#property-send)
  - [`reach`](#property-reach)
  - [`receive`](#property-receive)
  - [`ping`](#property-ping)

### メソッド

### _property_ **send**

サーバーにリクエストを送信した時間

- 種類:
  - [_float_](https://docs.python.org/3/library/functions.html#float)

### _property_ **reach**

サーバーでリクエストを処理した時間

- 種類:
  - [_float_](https://docs.python.org/3/library/functions.html#float)

### _property_ **receive**

レスポンスを処理した時間

- 種類:
  - [_float_](https://docs.python.org/3/library/functions.html#float)

### _property_ **ping**

Ping 値（往復のレイテンシー）

- 種類:
  - [_float_](https://docs.python.org/3/library/functions.html#float)

## Exceptions

`Client`クラスで発生するエラーを表します。

### `exception HTTP_db_Exception`

`Client`クラスのベースの例外です。

### `exception DatabaseKeyError`

キーが存在しない場合に発生します。

### `exception DatabaseReadError`

サーバー側で読み込みエラーが発生した場合に発生します。

### `exception DatabaseWriteError`

サーバー側で書き込みエラーが発生した場合に発生します。

### `exception DatabaseDeleteError`

サーバー側で削除エラーが発生した場合に発生します。

### `exception DatabaseUnknownError`

サーバーとの接続などでエラーが発生した場合に発生します。

### `exception DatabaseAuthenticationError`

データベースがパスワードで保護されているが、パスワードが違う又はパスワードが設定されていない場合に発生します。  
パスワードはインスタンスの初期化時に設定できます。
