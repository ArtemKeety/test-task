import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/api")
async def func():
    return {"ok":"ok"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)