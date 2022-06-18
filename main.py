import traceback
import sanic
import os
import sys
import json
import joblib
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
# Simple and database manager using HTTP

sys.setrecursionlimit(10000)

app = sanic.Sanic(name="HTTP_db")

ApplicationDatas = {
    "title": "HTTP_db",
    "version": "1.1.1",
    "author": "nattyan-tv",
    "repository": "https://github.com/nattyan-tv/HTTP_db.git"
}


DATAS = {}
SETTING = None
INTKEY = False

try:
    SETTING = json.load(open(f'{sys.path[0]}/setting.json', 'r'))
except OSError as err:
    print("An error has occurred during opening setting file.\n(Permission...Exists...)\nERR:1")
    sys.exit(1)

if "address" not in SETTING or "port" not in SETTING or "debug" not in SETTING or "location" not in SETTING or "remotesave" not in SETTING or "extras" not in SETTING:
    print("The setting file is invalid.\nERR:2")
    sys.exit(2)


if not SETTING["remotesave"]:
    if not os.path.isfile(SETTING["location"]):
        joblib.dump(DATAS, SETTING["location"], compress=3)
    try:
        DATAS = joblib.load(SETTING["location"])
    except OSError:
        print("An error has occurred during opening database file.\n(Permission...)\nERR:4")
        sys.exit(4)
else:
    if not os.path.isfile(f"{sys.path[0]}/key.json"):
        print("The key file is not found.\nERR:8")
        sys.exit(8)
    try:
        KEYFILE = json.load(open(f'{sys.path[0]}/key.json', 'r'))
    except OSError as err:
        print("An error has occurred during opening key file.\n(Permission...)\nERR:16")
        sys.exit(16)
    SPREADSHEET_KEY = SETTING["location"]
    if "cell" not in SETTING:
        print("The setting file is invalid.\nERR:2")
        sys.exit(2)
    CELL = SETTING["cell"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            KEYFILE, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
        gc = gspread.authorize(credentials)
        WORKSHEET = gc.open_by_key(SPREADSHEET_KEY).sheet1
        DATAS = json.loads(WORKSHEET.acell(CELL).value)
    except Exception as err:
        print("Cannot connect to database server.\nERR:32")
        sys.exit(32)


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


def convertReadAll() -> dict:
    rtData = {}
    for i in DATAS.keys():
        if i[:1] == "i":
            rtData[int(i[1:])] = DATAS[i]
        elif i[:1] == "s":
            rtData[str(i[1:])] = DATAS[i]
    return rtData


def convertWriteAll() -> dict:
    rtData = {}
    for i in DATAS.keys():
        if type(i) == int:
            rtData[f"i{i}"] = DATAS[i]
        elif type(i) == str:
            rtData[f"s{i}"] = DATAS[i]
    return rtData


def convertRead(data: dict) -> dict:
    rtData = {}
    for i in data.keys():
        if i[:1] == "i":
            rtData[int(i[1:])] = data[i]
        elif i[:1] == "s":
            rtData[str(i[1:])] = data[i]
    return rtData


def convertWrite(data: dict) -> dict:
    rtData = {}
    for i in data.keys():
        if type(i) == int:
            rtData[f"i{i}"] = data[i]
        elif type(i) == str:
            rtData[f"s{i}"] = data[i]
    return rtData


if "intkey" in SETTING["extras"]:
    convertReadAll()
    INTKEY = True


@app.get("/info")
async def Info(request):
    return sanic.response.json(ApplicationDatas)


@app.get("/ping")
async def Ping(request):
    return sanic.response.json({"status": "success", "time": datetime.datetime.now().timestamp()})


@app.get("/get_all")
async def GetAll(request):
    if INTKEY:
        return sanic.response.json(convertWriteAll())
    else:
        return sanic.response.json(DATAS)


@app.get("/get/<key>")
async def getResponse(request, key):
    try:
        rtData = {}
        if INTKEY:
            print(list(convertRead({key: None}).keys())[0])
            key = list(convertRead({key: None}).keys())[0]
        if key not in DATAS:
            rtData = {"status": "error", "description": "invalid key."}
        else:
            rtData = {"status": "success", "value": DATAS[key]}
        return sanic.response.json(rtData)
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


@app.get("/exists/<key>")
async def checkExists(request, key):
    if INTKEY:
        key = list(convertRead({key: None}).keys())[0]
    if key not in DATAS:
        return sanic.response.json({"exist": False})
    else:
        return sanic.response.json({"exist": True})


@app.get("/reload")
async def Reload(request):
    try:
        global DATAS
        DATAS = joblib.load(SETTING["location"])
        return sanic.response.json({"status": "success"})
    except OSError:
        return sanic.response.json({"status": "error", "description": "cannot open database file."})


@app.post("/post")
async def postResponse(request):
    try:
        js = request.json
        if INTKEY:
            js = convertRead(request.json)
        DATAS.update(js)
        await SaveDatabase()
        return sanic.response.json({"status": "success"})
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


@app.delete("/delete/<key>")
async def deleteResponse(request, key):
    try:
        if INTKEY:
            key = list(convertRead({key: None}).keys())[0]
        if key not in DATAS:
            return sanic.response.json({"status": "error", "description": "invalid key."})
        else:
            del DATAS[key]
            await SaveDatabase()
            return sanic.response.json({"status": "success"})
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


@app.delete("/delete_all")
async def deleteAll(request):
    try:
        DATAS.clear()
        await SaveDatabase()
        return sanic.response.json({"status": "success"})
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


if __name__ == '__main__':
    print(f"""\
HTTP_db
Simple and easy database manager using HTTP.

Tw: @nattyan_tv
GH: @nattyan-tv

Address: {SETTING['address']}:{SETTING['port']}
Debug: {SETTING['debug']}
Remote: {SETTING['remotesave']}
Location: {SETTING['location']}""")

    app.run(host=SETTING["address"],
            port=SETTING["port"], debug=SETTING["debug"])
