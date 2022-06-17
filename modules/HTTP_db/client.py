from .Exceptions import HTTP_db_Exception

import aiohttp
import datetime
# This is the module version of HTTP_db
# Simple and database manager using HTTP


def convertRead(data: dict) -> dict:
    """['i2021'] -> [2021]"""
    rtData = {}
    for i in data.keys():
        if i.startswith("i"):
            rtData[int(i[1:])] = data[i]
        elif i.startswith("s"):
            rtData[str(i[1:])] = data[i]
    return rtData


def convertWrite(data: dict) -> dict:
    """[2021] -> ['i2021']"""
    rtData = {}
    for i in data.keys():
        if type(i) == int:
            rtData[f"i{i}"] = data[i]
        elif type(i) == str:
            rtData[f"s{i}"] = data[i]
    return rtData


def keyConvertRead(key: str) -> str or int:
    """['i2021'] -> [2021]"""
    if key.startswith("i"):
        return int(key[1:])
    elif key.startswith("s"):
        return str(key[1:])
    else:
        raise HTTP_db_Exception("Unknown key type")


def keyConvertWrite(key: str or int) -> str:
    """[2021] -> ['i2021']"""
    if type(key) == int:
        return f"i{key}"
    elif type(key) == str:
        return f"s{key}"
    else:
        raise HTTP_db_Exception("Unknown key type")


class Ping():
    """\
HTTP_db Ping object  

- Method  

`send`: リクエストを送った時間  

`reach`: サーバーでリクエストを処理した時間  

`receive`: サーバーからレスポンスを受け取った時間  

`ping`: Ping値"""
    def __init__(self, send: float, reach: float, receive: float):
        self.send = send
        self.reach = reach
        self.receive = receive
        self.ping: float = receive - send


class Client():
    def __init__(self, url: str, port: int, intkey: bool = False):
        self.url = url
        self.port = port
        self.intkey = intkey

    async def info(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self.url}:{self.port}/info") as resp:
                return await resp.json()

    async def ping(self) -> float:
        now = datetime.datetime.now().timestamp()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self.url}:{self.port}/ping") as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    ping = Ping(
                        send=now,
                        reach=float(responseData["time"]),
                        receive=datetime.datetime.now().timestamp()
                    )
                    return ping
                else:
                    raise HTTP_db_Exception.UnknownDatabaseError()

    async def exists(self, key: str or int) -> bool:
        async with aiohttp.ClientSession() as session:
            if self.intkey is True:
                if type(key) is int:
                    key = f"i{key}"
                elif type(key) is str:
                    key = f"s{key}"
            async with session.get(f"http://{self.url}:{self.port}/exists/{key}") as r:
                responseData = await r.json()
                return bool(responseData["exist"])

    async def reload(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self.url}:{self.port}/reload") as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    raise HTTP_db_Exception.DatabaseIOError()
                else:
                    raise HTTP_db_Exception.UnknownDatabaseError()

    async def get(self, key: str or int):
        async with aiohttp.ClientSession() as session:
            if self.intkey:
                key = keyConvertWrite(key=key)
            async with session.get(f"http://{self.url}:{self.port}/get/{key}") as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return responseData["value"]
                elif responseData["status"] == "error":
                    if responseData["description"] == "invalid key.":
                        raise HTTP_db_Exception.DatabaseKeyError(
                            responseData["description"]
                        )
                    else:
                        raise HTTP_db_Exception.DatabaseReadError(
                            responseData["description"]
                        )
                else:
                    raise HTTP_db_Exception.UnknownDatabaseError()

    async def get_all(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self.url}:{self.port}/get_all") as r:
                responseData = await r.json()
                if self.intkey:
                    return convertRead(responseData)
                return responseData

    async def post(self, key: str or int, value: str or int or list or tuple or dict):
        if self.intkey:
            key = keyConvertWrite(key=key)
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://{self.url}:{self.port}/post", json={key: value}) as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    raise HTTP_db_Exception.DatabaseWriteError(
                        responseData["description"]
                    )
                else:
                    raise HTTP_db_Exception.UnknownDatabaseError()

    async def delete(self, key: str or int):
        if self.intkey:
            key = keyConvertWrite(key=key)
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://{self.url}:{self.port}/delete/{key}") as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    if responseData["description"] == "invalid key.":
                        raise HTTP_db_Exception.DatabaseKeyError(
                            responseData["description"]
                        )
                    else:
                        raise HTTP_db_Exception.DatabaseDeleteError(
                            responseData["description"]
                        )
                else:
                    raise HTTP_db_Exception.UnknownDatabaseError()

    async def delete_all(self):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://{self.url}:{self.port}/delete_all") as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    raise HTTP_db_Exception.DatabaseDeleteError(
                        responseData["description"]
                    )
                else:
                    raise HTTP_db_Exception.UnknownDatabaseError()


Client("localhost", 8080)
