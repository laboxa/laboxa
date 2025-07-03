from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.endpoints import face_recognition

from config import AppConfig
from database import DatabaseManager
from models import AttendanceRequest, HealthResponse
from pydantic import BaseModel
from PIL import Image
import io
import base64
import cv2
import numpy as np
import pose_recognition

check_fingers = False

# 環境変数を読み込み
load_dotenv()

# 設定とデータベース管理の初期化
config = AppConfig.from_env()
db_manager = DatabaseManager(config.database)

app = FastAPI(title="勤怠管理システム API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "勤怠管理システム API"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        with db_manager.get_connection() as connection:
            return HealthResponse(status="healthy", database="connected")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/attendance")
async def create_attendance(request: AttendanceRequest):
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO attendance_logs (user_name, type) 
                VALUES (%s, %s)
            """, (request.user_name, request.type))
            
        return {"message": "Attendance recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance")
async def get_attendance_logs():
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, user_name, type, timestamp 
                FROM attendance_logs 
                ORDER BY timestamp DESC
            """)
            
            logs = cursor.fetchall()
            return {"data": logs}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/users/status")
async def get_users_status():
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.name, 
                       COALESCE(al.type, 'checkout') as status,
                       al.timestamp as last_action_time
                FROM users u
                LEFT JOIN (
                    SELECT user_name, type, timestamp,
                           ROW_NUMBER() OVER (PARTITION BY user_name ORDER BY timestamp DESC) as rn
                    FROM attendance_logs
                ) al ON u.name = al.user_name AND al.rn = 1
                ORDER BY u.name
            """)
            
            users_status = cursor.fetchall()
            return {"data": users_status}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/users")
async def get_users():
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name 
                FROM users 
                ORDER BY name
            """)
            
            users = cursor.fetchall()
            return {"data": users}
    except Exception as e:
        return {"error": str(e)}

app.include_router(face_recognition.router, prefix="/face_recognition", tags=["Face_recognition"])


@app.post("/estimate_pose/")
async def estimate_pose(request: Request):
    form = await request.form()
    file = form['ufile']
    bf = await file.read()
    img_bin = io.BytesIO(bf)
    image = Image.open(img_bin).convert("RGB")
    numpy_image = np.array(image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    result = pose_recognition.detect_hand_gesture(opencv_image, check_fingers)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
