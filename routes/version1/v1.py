from fastapi import APIRouter

app_v1 = APIRouter()


@app_v1.get("/hello", )
async def hello_world():
    return {"Hello FastAPI! Version1"}
