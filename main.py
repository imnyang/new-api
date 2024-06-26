from sanic import Sanic
from sanic.response import text
from sanic.response import json
import func
import requests
import binascii

app = Sanic(
    "apimnyang",
)
app.config.OAS = False

@app.get("/")
async def root(request):
    return text("imnyang's API v2.0.0 (https://api.imnyang.xyz)\nIssue: me@imnyang.xyz\n\nWith sanic")

@app.get("/hex/encode/<text>")
async def hex_encode(request, text:str):
    return text(binascii.hexlify(text.encode()).decode())

@app.post("/website/send")
async def send(request):
    message = request.args.get('message')  # fetch 'message' from query parameters
    if not message:
        message = request.json.get('message')  # fetch 'message' from JSON body if it's JSON

    result = requests.post("https://discord.com/api/webhooks/1224283449427497011/U5EnBi0FZ9UB1c6fc-Je1vdgCj8mvRqJLWUZjN588_qxegggpIDTWG4ciiMNyayR1R6K", json = {
        "content" : message,
        "username" : request.ip
    })
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return json({"success": False, "error": err})

    else:
        return json({"success": True})

@app.get("/hex/decode/<hex>")
async def hex_decode(request, hex:str):
    try:
        return text(binascii.unhexlify(hex).decode())
    except binascii.Error as e:
        return text(e)

@app.get("/neis/search/<school>")
async def neis_search(request, school:str):
    '''
    검색어와 가장 비슷한 학교명을 리턴합니다.
    '''
    return json(func.get_school(school))

@app.get("/comci/search/<school>")
async def comci_search(request, school:str):
    '''
    검색어와 가장 비슷한 컴시간 학교 코드를 리턴합니다.
    '''
    return json(func.get_comci_school_code(school))

@app.get("/comci/get/<school>/<grade>/<cls>/<next_week>")
async def comci_get(request, school:str, grade:int, cls:int, next_week:bool):
    '''
    검색어와 가장 비슷한 학교명을 리턴합니다.
    '''
    return json(func.get_timetable(school, grade, cls, next_week))
