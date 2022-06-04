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

<details>
<summary>書き込み値の例</summary>

```json
{
    "keyname":"items"
}
```
</details>

<details>
<summary>戻り値の例</summary>

- 成功
```json
{
    "status":"success"
}
```

- 失敗
```json
{
    "status":"error",
    "description":"エラー内容"
}
```
</details>


## データの読み込み
概要|値
---|---
エンドポイント|`/get/<key>`
メソッド|`GET`
戻りデータ形式|`json/application`

`<key>`に対応するデータベースの値が`JSON`形式で送信されます。  
キーが存在しない場合は`description`に`invalid key.`が渡されて、`status`が`error`で返ります。

<details>
<summary>戻り値の例</summary>

- 成功
```json
{
    "status":"success",
    "value":"{'name':'nattyantv'}"
}
```

- 失敗
```json
{
    "status":"error",
    "description":"エラー内容"
}
```
</details>

