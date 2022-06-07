# This is the module version of HTTP_db

import sanic
import os, sys, json, asyncio
import joblib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
sys.setrecursionlimit(10000)

# Simple and database manager using HTTP

DATAS = {}

async def SaveDatabase():
    if SETTING["remotesave"]:
        await SaveDatabaseRemote()
    else:
        await SaveDatabaseLocal()


async def SaveDatabaseLocal():
    joblib.dump(DATAS, SETTING["location"], compress=3)
    return None


async def SaveDatabaseRemote():
    WORKSHEET.update_acell(CELL, json.dumps(DATAS))
    return None

app = sanic.Sanic(name="HTTP_db")

class HTTP_db():
    def __init__(self, url:str, port:int, filename:str):
        self.url = url
        self.port = port
        self.filename = filename


    def run(self):
        app.run(host=self.url, port=self.port)


    @app.get("/info")
    async def Info(request):
        return sanic.response.json({"title":"HTTP_db module edition"})


    @app.get("/get_all")
    async def GetAll(request):
        return sanic.response.json(DATAS)


    @app.get("/get/<key>")
    async def getResponse(request, key):
        try:
            rtData = {}
            if key not in DATAS:
                rtData = {"status":"error","description":"invalid key."}
            else:
                rtData = {"status":"success","value":DATAS[key]}
            return sanic.response.json(rtData)
        except Exception as err:
            return sanic.response.json({"status":"error","description":err})


    @app.post("/post")
    async def postResponse(request):
        try:
            DATAS.update(request.json)
            await SaveDatabase()
            return sanic.response.json({"status":"success"})
        except Exception as err:
            return sanic.response.json({"status":"error","description":err})


    @app.delete("/delete/<key>")
    async def deleteResponses(request, key):
        try:
            if key not in DATAS:
                return sanic.response.json({"status":"error","description":"invalid key."})
            else:
                del DATAS[key]
                await SaveDatabase()
                return sanic.response.json({"status":"success"})
        except Exception as err:
            return sanic.response.json({"status":"error","description":err})


    @app.delete("/delete_all")
    async def deleteAll(request):
        try:
            DATAS.clear()
            await SaveDatabase()
            return sanic.response.json({"status":"success"})
        except Exception as err:
            return sanic.response.json({"status":"error","description":err})

