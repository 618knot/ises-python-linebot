from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hoge():
    return "hoge"