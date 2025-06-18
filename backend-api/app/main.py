from fastapi import FastAPI
from api.endpoints import test, face_recognition

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(test.router, prefix="/test", tags=["Test"])
app.include_router(face_recognition.router, prefix="/face_recognition", tags=["Face_recognition"])