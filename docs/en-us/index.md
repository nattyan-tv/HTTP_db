# API Reference
`HTTP_db` is simple and easy database manager using HTTP.

## Write data

Description|Value
---|---
Endpoint|`/post`
Method|`POST`
Send data type|`json/application`
Return data type|`json/application`

Pass the value to write in `JSON` format.  
The database dictionary will be updated with the value of the passed JSON.  
If JSON with the same key is passed, the dictionary will be overwritten.

<details>
<summary>Example of write</summary>


```json
{
    "keyname":"items"
}
```

</details>

<details>
<summary>Example of return</summary>

- Success

```json
{
    "status":"success"
}
```

- Failed

```json
{
    "status":"error",
    "description":"Detail of error"
}
```

</details>


## Read data

Description|Value
---|---
Endpoint|`/get/<key>`
Method|`GET`
Return data type|`json/application`

The value of the database corresponding to `<key>` is sent in `JSON` format.  
If the key does not exist, `invalid key.` is passed to `description` and `status` returns `error`.

<details>
<summary>Example of return</summary>

- Success

```json
{
    "status":"success",
    "value":"{'name':'nattyantv'}"
}
```

- Failed

```json
{
    "status":"error",
    "description":"Detail of error"
}
```

</details>

