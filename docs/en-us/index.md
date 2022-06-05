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

- Example of write  

```json
{
    "keyname":"items"
}
```


- Example of return  

__Success__

```json
{
    "status":"success"
}
```

__Failed__

```json
{
    "status":"error",
    "description":"Detail of error"
}
```



## Read data

Description|Value
---|---
Endpoint|`/get/<key>`
Method|`GET`
Return data type|`json/application`

The value of the database corresponding to `<key>` is sent in `JSON` format.  
If the key does not exist, `invalid key.` is passed to `description` and `status` returns `error`.

- Example of return  

__Success__

```json
{
    "status":"success",
    "value":"{'name':'nattyantv'}"
}
```

__Failed__

```json
{
    "status":"error",
    "description":"Detail of error"
}
```


## Delete data

Description|Value
---|---
Endpoint|`/delete/<key>`
Method|`DELETE`
Return data type|`json/application`

Deletes the value passed to `key` from the database.
If the key does not exist, `invalid key.` is passed to `description` and `status` returns `error`.

- Example of return  

__Success__

```json
{
    "status":"success"
}
```

__Failed__

```json
{
    "status":"error",
    "description":"Detail of error"
}
```

