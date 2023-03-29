from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aiohttp
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")
templates = Jinja2Templates(directory="./app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

parter_technikum = [0, 1, 2,  4, 5]
pietro_technikum = [6, 7, 8, 9, 10, 11]
parter_liceum = [12, 13, 14, 15, 16]
pietro_liceum = [17, 18, 19, 20, 21, 22]
pozostale = [23, 24, 25, 26, 27, 28]
nazwy_sal: dict[int: str] = {0: "L0.07", 1: "L0.09", 2: "L0.10", 4: "L0.13", 5: "L0.14", 6: "L1.06a", 7: "L1.06b", 8: "L1.09", 9: "L1.10", 10: "L1.13", 11: "L1.14",
                             12: "G0.07", 13: "G0.09", 14: "G0.10", 15: "G0.13", 16: "G0.14", 17: "G1.06a", 18: "G1.06b", 19: "G1.09", 20: "G1.10", 21: "G1.13", 22: "G1.14", 23: "S1.22", 24: "S1.23", 25: "Hala",26:"Biblioteka",27:"Sala Letnia (szachy)", 28:"Internat"}
sala: dict[str:int] = {'l007': 0, 'l009': 1, 'l010': 2, 'l013': 4, 'l014': 5, 'l106a': 6, 'l106b': 7, 'l109': 8, 'l110': 9, 'l113': 10, 'l114': 11, 'g007': 12,
                       'g009': 13, 'g010': 14, 'g013': 15, 'g014': 16, 'g106a': 17, 'g106b': 18, 'g109': 19, 'g110': 20, 'g113': 21, 'g114': 22, 's122': 23, 's123': 24, 'hala': 25, 'biblioteka':26, 'szachy':27, 'internat':28}
sala_zajeta: dict[int: bool] = {0: False, 1: False, 2: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False, 11: False,
                                12: False, 13: False, 14: False, 15: False, 16: False, 17: False, 18: False, 19: False, 20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26:False, 27:False, 28:False}

# asyncio.set_event_loop_policy(
#     asyncio.WindowsSelectorEventLoopPolicy())  # delete on linux0


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {'request': request, "parter_technikum": parter_technikum, "pietro_technikum": pietro_technikum, "parter_liceum": parter_liceum, "pietro_liceum": pietro_liceum, "pozostale": pozostale, "nazwy_sal": nazwy_sal, "sala": sala, "sala_zajeta": sala_zajeta})


@app.post("/sala/change/{idc}", response_class=HTMLResponse)
def zmien(idc):
    idc = int(idc)
    sala_zajeta[idc] = not sala_zajeta[idc]
    return "done"


@app.get("/sala/{idc}", response_class=HTMLResponse)
def search(idc, request: Request) -> HTMLResponse:
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
        text= "Zajmij"

    return templates.TemplateResponse("manage.html", {'request': request, 'classroom_name': classroom_name, 'classroom_status': classroom_status, 'classroom_id': classroom_id, 'header': header, 'floor': floor,'style':style,'text':text})


@app.get("/rzepus_rzepec", response_class=HTMLResponse)
def rzepa_rzepecki(request: Request) -> HTMLResponse:
    ile = list(sala_zajeta.keys())
    return templates.TemplateResponse("admin.html", {'request': request,"sala_zajeta":sala_zajeta,"nazwy_sal":nazwy_sal,"ile":ile})

if __name__ == "__main__":
    uvicorn.run(app, port=80)
