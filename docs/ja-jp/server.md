# API リファレンス(サーバー)

`HTTP_db`は、HTTP を使用してデータの書き込みや読み込みを行う、簡易的かつとっつき易い、データベースマネージャーです。

## データの書き込み

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/post`            |
| メソッド       | `POST`             |
| 送信データ形式 | `json/application` |
| 戻りデータ形式 | `json/application` |

書き込みには`JSON`形式で値を渡します。  
渡された JSON の値でデータベースの辞書が更新されます。  
同一キーだった場合は上書きされます。

- 書き込み値の例

```json
{
  "keyname": "items"
}
```

- 戻り値の例

**成功**

```json
{
  "status": "success"
}
```

**失敗**

```json
{
  "status": "error",
  "description": "エラー内容"
}
```

## データの読み込み

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/get/<key>`       |
| メソッド       | `GET`              |
| 戻りデータ形式 | `json/application` |

`<key>`に対応するデータベースの値が`JSON`形式で送信されます。  
キーが存在しない場合は`description`に`invalid key.`が渡されて、`status`が`error`で返ります。

- 戻り値の例

**成功**

```json
{
  "status": "success",
  "value": "{'name':'nattyantv'}"
}
```

**失敗**

```json
{
  "status": "error",
  "description": "エラー内容"
}
```

## データの全読み込み

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/get_all`         |
| メソッド       | `GET`              |
| 戻りデータ形式 | `json/application` |

すべてのデータベースの値が`JSON`形式で送信されます。

- 戻り値の例

```json
{
  "name": "nattyantv",
  "age": -999,
  "address": "Earth"
}
```

## データの削除

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/delete/<key>`    |
| メソッド       | `DELETE`           |
| 戻りデータ形式 | `json/application` |

`<key>`に対応するデータベースの値を削除します。  
キーが存在しない場合は`description`に`invalid key.`が渡されて、`status`が`error`で返ります。

- 戻り値の例

**成功**

```json
{
  "status": "success"
}
```

**失敗**

```json
{
  "status": "error",
  "description": "エラー内容"
}
```

## データの全削除

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/delete_all`      |
| メソッド       | `DELETE`           |
| 戻りデータ形式 | `json/application` |

データベースのすべての値を削除します。

- 戻り値の例

**成功**

```json
{
  "status": "success"
}
```

**失敗**

```json
{
  "status": "error",
  "description": "エラー内容"
}
```

## Ping レスポンス

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/ping`            |
| メソッド       | `GET`              |
| 戻りデータ形式 | `json/application` |

サーバーでリクエストを処理した時間を返します。  
時間は Unix タイムスタンプで返されます。

- 戻り値の例

```json
{
  "status": "success",
  "time": 123456789.12345679
}
```

## キーの存在チェック

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/exists/<key>`    |
| メソッド       | `GET`              |
| 戻りデータ形式 | `json/application` |

`JSON`が返ってきます。  
データベースのキーに`<key>`が存在した場合は`exist`に`true`、存在しない場合は`false`を返します。

- 戻り値の例

**存在した場合**

```json
{
  "exist": true
}
```

**存在しなかった場合**

```json
{
  "exist": false
}
```

## キーの存在チェック

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/exists/<key>`    |
| メソッド       | `GET`              |
| 戻りデータ形式 | `json/application` |

`JSON`が返ってきます。  
データベースのキーに`<key>`が存在した場合は`exist`に`true`、存在しない場合は`false`を返します。

- 戻り値の例

**存在した場合**

```json
{
  "exist": true
}
```

**存在しなかった場合**

```json
{
  "exist": false
}
```

## データベースの再読み込み

| 概要           | 値                 |
| -------------- | ------------------ |
| エンドポイント | `/reload`          |
| メソッド       | `GET`              |
| 戻りデータ形式 | `json/application` |

データベースのファイル及びリモートから変数を再読み込みします。

- 戻り値の例

**成功**

```json
{
  "status": "success"
}
```

**失敗**

```json
{
  "status": "error",
  "description": "cannot open database file."
}
```