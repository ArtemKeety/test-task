import uvicorn
from fastapi import FastAPI
from db import DataBase
from routers import *


app = FastAPI()


@app.get("/api")
async def func():
    await DataBase.check_connection()
    return {"ok": "ok"}

app.include_router(DishRouter, prefix="/api", tags=["dish"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)