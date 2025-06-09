from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def test_get():
    return {"message": "Hello from test"}