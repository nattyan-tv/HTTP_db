import sanic
import os, sys, json
import joblib

# Simple and database manager using HTTP

sys.setrecursionlimit(10000)

app = sanic.Sanic(name="HTTP_db")

ApplicationDatas = {
    "title":"HTTP_db",
    "version":"0.9.1",
    "author":"nattyan-tv",
    "repository":"https://github.com/nattyan-tv/HTTP_db.git"
}


DATAS = {}
SETTING = None

try: SETTING = json.load(open(f'{sys.path[0]}/setting.json', 'r'))
except OSError as err: print("An error has occurred during opening setting file.\n(Permission...Exists...)\nERR:1"); sys.exit(1)

if "address" not in SETTING or "port" not in SETTING or "debug" not in SETTING or "filename" not in SETTING: print("The setting file is invalid.\nERR:2"); sys.exit(2)

if not os.path.isfile(SETTING["filename"]): joblib.dump(DATAS, SETTING["filename"], compress=3)
try: DATAS = joblib.load(SETTING["filename"])
except OSError: print("An error has occurred during opening database file.\n(Permission...)\nERR:4"); sys.exit(4)


async def SaveDatabase():
    joblib.dump(DATAS, SETTING["filename"], compress=3)
    return None


@app.route("/info")
async def Info(request):
    return sanic.response.json(ApplicationDatas)


@app.route("/get/<key>")
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
async def deleteResponse(request, key):
    try:
        if key not in DATAS:
            return sanic.response.json({"status":"error","description":"invalid key."})
        else:
            del DATAS[key]
            await SaveDatabase()
            return sanic.response.json({"status":"success"})
    except Exception as err:
        return sanic.response.json({"status":"error","description":err})



if __name__ == '__main__':
    print(f"""\
HTTP_db
Simple and easy database manager using HTTP.

Tw: @nattyan_tv
GH: @nattyan-tv

Address: {SETTING['address']}:{SETTING['port']}
Debug: {SETTING['debug']}
Filename: {SETTING['filename']}""")
    app.run(host=SETTING["address"], port=SETTING["port"], debug=SETTING["debug"])
