import uvicorn
from fastapi import FastAPI
from routers import *


app = FastAPI()


app.include_router(DishRouter, prefix="/api", tags=["dish"])
app.include_router(OrderRouter, prefix="/api", tags=["order"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)