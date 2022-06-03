import sanic
import os, sys, json

app = sanic.Sanic(name="Sanic")

DATAS = {}
SETTING = None

try: SETTING = json.load(open(f'{sys.path[0]}/setting.json', 'r'))
except OSError as err: print("An error has occurred during file opening\n(Permission...Exists...)"); sys.exit(1)

if "address" not in SETTING or "port" not in SETTING or "debug" not in SETTING: print("The setting file is invalid."); sys.exit(2)

@app.route("/get/<key>")
async def getResponse(request, key):
    rtData = None
    if key not in DATAS:
        rtData = {}
    else:
        rtData = DATAS[key]
    return sanic.response.json(rtData)


@app.post("/post")
async def postResponse(request):
    try:
        DATAS.update(request.json)
        return sanic.response.json({"status":"success"})
    except BaseException as err:
        return sanic.response.json({"status":"error","description":err})

if __name__ == '__main__':
    app.run(host=SETTING["address"], port=SETTING["port"], debug=SETTING["debug"])
