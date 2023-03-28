import fastapi
import uvicorn
from os import path

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
