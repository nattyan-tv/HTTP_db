from .Exceptions import HTTP_db_Exception

import aiohttp
# This is the module version of HTTP_db
# Simple and database manager using HTTP


class Client():
    def __init__(self, url: str, port: int):
        self.url = url
        self.port = port

    async def info(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self.url}:{self.port}/info") as resp:
                return await resp.json()

    async def get(self, key: str):
        async with aiohttp.ClientSession() as session:
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
                return responseData

    async def post(self, key: str, value: str or int or list or tuple or dict):
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

    async def delete(self, key: str):
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
