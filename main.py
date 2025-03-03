from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

# Serve static files from /static
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "WEBSOCKET"],
    allow_headers=["*"],
)


# Definitions of classrooms and statuses with ID 3 included
parter_technikum = [0, 1, 2, 3, 4, 5]
pietro_technikum = [6, 7, 8, 9, 10, 11]
parter_liceum = [12, 13, 14, 15, 16]
pietro_liceum = [17, 18, 19, 20, 21, 22]
pozostale = [23, 24, 25, 26, 27, 28]

nazwy_sal: dict[int, str] = {
    0: "L0.07", 1: "L0.09", 2: "L0.10", 3: "L0.11", 4: "L0.13", 5: "L0.14",
    6: "L1.06a", 7: "L1.06b", 8: "L1.09", 9: "L1.10", 10: "L1.13", 11: "L1.14",
    12: "G0.07", 13: "G0.09", 14: "G0.10", 15: "G0.13", 16: "G0.14",
    17: "G1.06a", 18: "G1.06b", 19: "G1.09", 20: "G1.10", 21: "G1.13", 22: "G1.14",
    23: "S1.22", 24: "S1.23", 25: "Hala", 26: "Biblioteka", 27: "Sala Letnia (szachy)", 28: "Internat"
}

sala: dict[str, int] = {
    'l007': 0, 'l009': 1, 'l010': 2, 'l011': 3, 'l013': 4, 'l014': 5,
    'l106a': 6, 'l106b': 7, 'l109': 8, 'l110': 9, 'l113': 10, 'l114': 11,
    'g007': 12, 'g009': 13, 'g010': 14, 'g013': 15, 'g014': 16,
    'g106a': 17, 'g106b': 18, 'g109': 19, 'g110': 20, 'g113': 21, 'g114': 22,
    's122': 23, 's123': 24, 'hala': 25, 'biblioteka': 26, 'sala_letnia': 27, 'internat': 28
}

# Ensure sala_zajeta now includes ID 3
sala_zajeta: dict[int, bool] = {key: False for key in nazwy_sal.keys()}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Updated WebSocket endpoint under /openday
@app.websocket("/openday/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# New root endpoint for Hello World
@app.get("/", response_class=HTMLResponse)
def hello_world():
    return HTMLResponse("<h1>Hello World</h1>")

# All app routes now use the /openday prefix
@app.get("/openday/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {
        'request': request,
        "parter_technikum": parter_technikum,
        "pietro_technikum": pietro_technikum,
        "parter_liceum": parter_liceum,
        "pietro_liceum": pietro_liceum,
        "pozostale": pozostale,
        "nazwy_sal": nazwy_sal,
        "sala": sala,
        "sala_zajeta": sala_zajeta
    })

@app.post("/openday/sala/change/{idc}", response_class=HTMLResponse)
async def zmien(idc: int):
    sala_zajeta[idc] = not sala_zajeta[idc]
    message = json.dumps({"classroom_id": idc, "status": sala_zajeta[idc]})
    await manager.broadcast(message)
    return "done"

@app.get("/openday/sala/{idc}", response_class=HTMLResponse)
def search(idc: str, request: Request) -> HTMLResponse:
    if idc not in sala:
        return "Błąd - Podaj poprawny numer sali lub skontaktuj się z Rzepeckim"
    classroom_id = sala[idc]
    classroom_name = nazwy_sal[classroom_id]
    classroom_status = sala_zajeta[classroom_id]
    if classroom_id in parter_technikum or classroom_id in pietro_technikum:
        header = "Technikum"
    elif classroom_id in parter_liceum or classroom_id in pietro_liceum:
        header = "Liceum"
    elif classroom_id in pozostale:
        header = "Pozostałe"
    else:
        header = "Błąd"

    if classroom_id in parter_technikum or classroom_id in parter_liceum:
        floor = "parter"
    elif classroom_id in pietro_technikum or classroom_id in pietro_liceum:
        floor = "piętro"
    elif classroom_id in pozostale:
        floor = None
    else:
        floor = "Błąd"

    if sala_zajeta[classroom_id]:
        style = "zajete"
        text = "Zwolnij"
    else:
        style = "wolne"
        text = "Zajmij"

    return templates.TemplateResponse("manage.html", {
        'request': request,
        'classroom_name': classroom_name,
        'classroom_status': classroom_status,
        'classroom_id': classroom_id,
        'header': header,
        'floor': floor,
        'style': style,
        'text': text,
        'sala_zajeta': sala_zajeta,
    })

@app.get("/openday/rzepus_rzepec", response_class=HTMLResponse)
def rzepa_rzepecki(request: Request) -> HTMLResponse:
    ile = list(sala_zajeta.keys())
    return templates.TemplateResponse("admin.html", {
        'request': request,
        "sala_zajeta": sala_zajeta,
        "nazwy_sal": nazwy_sal,
        "ile": ile
    })

if __name__ == "__main__":
    uvicorn.run(app, port=80)
