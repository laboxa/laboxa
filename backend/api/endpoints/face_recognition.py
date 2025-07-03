from fastapi import APIRouter, Request
from services import face_recognition_service as service
from PIL import Image
import io

router = APIRouter()

@router.post("/inference")
async def inference_post(request: Request):
    form = await request.form()
    file = form['ufile']
    bf = await file.read()
    img_bin = io.BytesIO(bf)
    image = Image.open(img_bin)
    result = service.inference(image)
    return result

@router.post("/checkin")
async def inference_post(request: Request):
    form = await request.form()
    file = form['ufile']
    bf = await file.read()
    img_bin = io.BytesIO(bf)
    image = Image.open(img_bin)
    result = service.checkin(image)
    return result

@router.post("/checkout")
async def inference_post(request: Request):
    form = await request.form()
    file = form['ufile']
    bf = await file.read()
    img_bin = io.BytesIO(bf)
    image = Image.open(img_bin)
    result = service.checkout(image)
    return result

@router.post("/upload_npy")
async def upload_npy_post(request: Request):
    form = await request.form()
    name = form['name']
    npy_file = form['npy_file']
    bf = await npy_file.read()
    service.upload(bf, name)

    return {"message": "done"}