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
    "version": "1.2.1",
    "author": "nattyan-tv",
    "repository": "https://github.com/nattyan-tv/HTTP_db.git"
}


DATAS = {}
SETTING = None
INTKEY = False
PASSWORD = None

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

if os.path.isfile("password"):
    with open("password", "r") as f:
        PASSWORD = f.read()


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


# def convertReadAll() -> dict:
#    rtData = {}
#    for i in DATAS.keys():
#        if i[:1] == "i":
#            rtData[int(i[1:])] = DATAS[i]
#        elif i[:1] == "s":
#            rtData[str(i[1:])] = DATAS[i]
#    return rtData
#
#
# def convertWriteAll() -> dict:
#    rtData = {}
#    for i in DATAS.keys():
#        if type(i) == int:
#            rtData[f"i{i}"] = DATAS[i]
#        elif type(i) == str:
#            rtData[f"s{i}"] = DATAS[i]
#    return rtData
#
#
# def convertRead(data: dict) -> dict:
#    rtData = {}
#    for i in data.keys():
#        if i[:1] == "i":
#            rtData[int(i[1:])] = data[i]
#        elif i[:1] == "s":
#            rtData[str(i[1:])] = data[i]
#    return rtData
#
#
# def convertWrite(data: dict) -> dict:
#    rtData = {}
#    for i in data.keys():
#        if type(i) == int:
#            rtData[f"i{i}"] = data[i]
#        elif type(i) == str:
#            rtData[f"s{i}"] = data[i]
#    return rtData


@app.get("/info")
async def Info(request):
    return sanic.response.json(ApplicationDatas)


@app.get("/ping")
async def Ping(request):
    return sanic.response.json({"status": "success", "time": datetime.datetime.now().timestamp()})


@app.post("/get_all")
async def GetAll(request: sanic.Request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
    else:
        return sanic.response.json({"status": "success", "contents": [{"key": i, "value": DATAS[i]} for i in list(DATAS.keys())]})


@app.post("/get")
async def getResponse(request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
    try:
        key = request.json["key"]
        rtData = {}
        if key not in DATAS:
            rtData = {"status": "error", "description": "invalid key."}
        else:
            rtData = {"status": "success", "value": DATAS[key]}
        return sanic.response.json(rtData)
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


@app.post("/exists")
async def checkExists(request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
    key = request.json["key"]
    if key not in DATAS:
        return sanic.response.json({"exist": False})
    else:
        return sanic.response.json({"exist": True})


@app.post("/reload")
async def Reload(request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
    try:
        global DATAS
        DATAS = joblib.load(SETTING["location"])
        return sanic.response.json({"status": "success"})
    except OSError:
        return sanic.response.json({"status": "error", "description": "cannot open database file."})


@app.post("/post")
async def postResponse(request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
    try:
        js = request.json
        DATAS.update({js["key"]: js["value"]})
        await SaveDatabase()
        return sanic.response.json({"status": "success"})
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


@app.post("/delete")
async def deleteResponse(request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
    try:
        key = request.json["key"]
        if key not in DATAS:
            return sanic.response.json({"status": "error", "description": "invalid key."})
        else:
            del DATAS[key]
            await SaveDatabase()
            return sanic.response.json({"status": "success"})
    except Exception as err:
        return sanic.response.json({"status": "error", "description": repr(err)})


@app.post("/delete_all")
async def deleteAll(request):
    if PASSWORD is not None and "password" not in request.json or request.json["password"] != PASSWORD:
        return sanic.response.json({"status": "error", "description": "Authentication Failed"})
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

    app.run(
        host=SETTING["address"],
        port=SETTING["port"],
        debug=SETTING["debug"]
    )
