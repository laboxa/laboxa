from dotenv import load_dotenv

from config import AppConfig
from database import DatabaseManager
from models import AttendanceRequest, HealthResponse

# 環境変数を読み込み
load_dotenv()

# 設定とデータベース管理の初期化
config = AppConfig.from_env()
db_manager = DatabaseManager(config.database)

def set_attendance_logs(user_name, type):
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO attendance_logs (user_name, type)
                VALUES (%s, %s)
            """, (user_name, type))
        return True
    except Exception as e:
        print(e)
        return False

def get_current_type(user_name):
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                select type from attendance_logs
                where user_name=%s 
                    and timestamp = (select MAX(timestamp) from attendance_logs where user_name=%s);
            """, (user_name, user_name))
            
            type = cursor.fetchall()
            return {"data": type}
    except Exception as e:
        return {"data": str(e)}