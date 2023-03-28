from fastapi import FastAPI, Request

nazwy_sal = {0: "Sala 1", 1: "Sala 2", 2: "Sala 3"}
sale = {0: False, 1: True, 2: False}

@app.get("/sala/{id}")
def sala(id: int):
    sale[id] = not sale[id]
    return {"nazwa": nazwy_sal[id], "status": sale[id]}

@app.get("/admin")
def admin():
    return {"sale": sale}
