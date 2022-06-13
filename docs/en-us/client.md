# Info

`HTTP_db` is simple and easy database manager using HTTP.

# Usage

Initialize a `Client` instance.
Data acquisition and other operations can be performed by executing functions on the initialized instance.

```py
clinet = HTTP_db.Clinet("localhost", 8080)

datas = await client.get_all()
await client.post("temp", datas)
```

# API Reference

## Client

`class HTTP_db.Client(url, port)`

- Methods:
  - async [`info`](#await-info)
  - async [`get`](#await-get)
  - async [`get_all`](#await-getall)
  - async [`post`](#await-post)
  - async [`delete`](#await-delete)
  - async [`delete_all`](#await-deleteall)
- Parameters:
  - `url` ([str](https://docs.python.org/3/library/functions.html#func-str)): HTTP Server address
  - `port` ([int](https://docs.python.org/3/library/functions.html#int)): HTTP Server port

### Methods

### _await_ **info()**

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).  
It returns a [_dict_](https://docs.python.org/3/library/stdtypes.html#dict) that contains information about the server.

- Parameters:
  - None
- Return:
  - [_dict_](https://docs.python.org/3/library/stdtypes.html#dict)

### _await_ **get(_key_)**

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).  
It returns a [_dict_](https://docs.python.org/3/library/stdtypes.html#dict) that contains the data of the specified key.

- Parameters:
  - `key` ([str](https://docs.python.org/3/library/functions.html#func-str)): Data's key
- Raises:
  - [**`DatabaseKeyError`**](#exception-databasekeyerror) - If the specified key does not exist.
  - [**`DatabaseReadError`**](#exception-databasereaderror) - If the server returns an error.
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - If an error occurs in connection with the server, etc.
- Return:
  - [_dict_](https://docs.python.org/3/library/stdtypes.html#dict)

### _await_ **get_all()**

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).  
It returns a [_dict_](https://docs.python.org/3/library/stdtypes.html#dict) that contains all the data.

- Parameters:
  - None
- Raises:
  - [**`DatabaseReadError`**](#exception-databasereaderror) - If the server returns an error.
- Return:
  - [_dict_](https://docs.python.org/3/library/stdtypes.html#dict)

### _await_ **post(_key_, _data_)**

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).  
It writes the data of the specified key.

- Parameters:
  - `key` ([str](https://docs.python.org/3/library/functions.html#func-str)): Data's key
  - `data` ([_dict_](https://docs.python.org/3/library/stdtypes.html#dict)): Data value
- Raises:
  - [**`DatabaseWriteError`**](#exception-databasewriteerror) - If the server returns an error.
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - If an error occurs in connection with the server, etc.
- Return:
  - None

### _await_ **delete(_key_)**

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).  
It deletes the data of the specified key.

- Parameters:
  - `key` ([str](https://docs.python.org/3/library/functions.html#func-str)): Data's key
- Raises:
  - [**`DatabaseKeyError`**](#exception-databasekeyerror) - If the specified key does not exist.
  - [**`DatabaseDeleteError`**](#exception-databasedeleteerror) - If the server returns an error.
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - If an error occurs in connection with the server, etc.
- Return:
  - None

### _await_ **delete_all()**

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).  
It deletes all the data.

- Parameters:
  - None
- Raises:
  - [**`DatabaseDeleteError`**](#exception-databasedeleteerror) - If the server returns an error.
  - [**`DatabaseUnknownError`**](#exception-databaseunknownerror) - If an error occurs in connection with the server, etc.
- Return:
  - None

## Exceptions

The following exceptions are raised by the functions of the `Client` class.

### `exception HTTP_db_Exception`

Base exception class of the `Client` class.

### `exception DatabaseKeyError`

Raised when the specified key does not exist.

### `exception DatabaseReadError`

Raised when the server returns an error.

### `exception DatabaseWriteError`

Raised when the server returns an error.

### `exception DatabaseDeleteError`

Raised when the server returns an error.

### `exception DatabaseUnknownError`

Raised when the server application returns an error.
