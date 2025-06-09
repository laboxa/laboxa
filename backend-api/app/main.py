from fastapi import FastAPI
from api.endpoints import test

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(test.router, prefix="/test", tags=["Test"])