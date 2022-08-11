from .Exceptions import *

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
    def __init__(self, url: str = "http://localhost:8080", password: str = ""):
        self.url = url
        self.password = password

    async def info(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/info") as resp:
                return await resp.json()

    async def ping(self) -> Ping:
        now = datetime.datetime.now().timestamp()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/ping") as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    ping = Ping(
                        send=now,
                        reach=float(responseData["time"]),
                        receive=datetime.datetime.now().timestamp()
                    )
                    return ping
                else:
                    raise UnknownDatabaseError()

    async def auth(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/auth", json={"password": self.password}) as r:
                responseData = await r.json()
                if responseData["status"] == "error":
                    return False
                return True

    async def exists(self, key: str or int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/exists", json={"password": self.password, "keyname": key}) as r:
                responseData = await r.json()
                if responseData["status"] == "error":
                    if responseData["description"] == "Authentication Failed":
                        raise DatabaseAuthenticationError()
                    else:
                        raise UnknownDatabaseError()
                return bool(responseData["exist"])

    async def reload(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/reload", json={"password": self.password}) as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    raise DatabaseIOError()
                else:
                    raise UnknownDatabaseError()

    async def get(self, key: str or int):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/get", json={"password": self.password, "key": key}) as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return responseData["value"]
                elif responseData["status"] == "error":
                    if responseData["description"] == "invalid key.":
                        raise DatabaseKeyError(
                            responseData["description"]
                        )
                    else:
                        raise DatabaseReadError(
                            responseData["description"]
                        )
                else:
                    raise UnknownDatabaseError()

    async def get_all(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/get_all", json={"password": self.password}) as r:
                responseData = await r.json()
                if responseData["status"] == "error":
                    if responseData["description"] == "Authentication Failed":
                        raise DatabaseAuthenticationError()
                    else:
                        raise UnknownDatabaseError()
                return {i["key"]: i["value"] for i in responseData["contents"]}

    async def post(self, key: str or int, value: str or int or list or tuple or dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/post", json={"password": self.password, "key": key, "value": value}) as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    if responseData["description"] == "Authentication Failed":
                        raise DatabaseAuthenticationError()
                    else:
                        raise DatabaseWriteError(
                            responseData["description"]
                        )
                else:
                    raise UnknownDatabaseError()

    async def delete(self, key: str or int):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/delete", json={"password": self.password, "key": key}) as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    if responseData["description"] == "invalid key.":
                        raise DatabaseKeyError(
                            responseData["description"]
                        )
                    elif responseData["description"] == "Authentication Failed":
                        raise DatabaseAuthenticationError()
                    else:
                        raise DatabaseDeleteError(
                            responseData["description"]
                        )
                else:
                    raise UnknownDatabaseError()

    async def delete_all(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/delete_all", json={"password": self.password}) as r:
                responseData = await r.json()
                if responseData["status"] == "success":
                    return None
                elif responseData["status"] == "error":
                    if responseData["description"] == "Authentication Failed":
                        raise DatabaseAuthenticationError()
                    else:
                        raise DatabaseDeleteError(
                            responseData["description"]
                        )
                else:
                    raise UnknownDatabaseError()
