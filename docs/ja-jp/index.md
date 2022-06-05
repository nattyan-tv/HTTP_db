# APIリファレンス
`HTTP_db`は、HTTPを使用してデータの書き込みや読み込みを行う、簡易的かつとっつき易い、データベースマネージャーです。

## データの書き込み

概要|値
---|---
エンドポイント|`/post`
メソッド|`POST`
送信データ形式|`json/application`
戻りデータ形式|`json/application`

書き込みには`JSON`形式で値を渡します。  
渡されたJSONの値でデータベースの辞書が更新されます。  
同一キーだった場合は上書きされます。

- 書き込み値の例  

```json
{
    "keyname":"items"
}
```

- 戻り値の例  

__成功__

```json
{
    "status":"success"
}
```

__失敗__

```json
{
    "status":"error",
    "description":"エラー内容"
}
```


## データの読み込み

概要|値
---|---
エンドポイント|`/get/<key>`
メソッド|`GET`
戻りデータ形式|`json/application`

`<key>`に対応するデータベースの値が`JSON`形式で送信されます。  
キーが存在しない場合は`description`に`invalid key.`が渡されて、`status`が`error`で返ります。

- 戻り値の例  

__成功__

```json
{
    "status":"success",
    "value":"{'name':'nattyantv'}"
}
```

__失敗__
```json
{
    "status":"error",
    "description":"エラー内容"
}
```


## データの削除

概要|値
---|---
エンドポイント|`/delete/<key>`
メソッド|`DELETE`
戻りデータ形式|`json/application`

`<key>`に対応するデータベースの値を削除します。
キーが存在しない場合は`description`に`invalid key.`が渡されて、`status`が`error`で返ります。

- 戻り値の例  

__成功__

```json
{
    "status":"success"
}
```

__失敗__

```json
{
    "status":"error",
    "description":"エラー内容"
}
```


