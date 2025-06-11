from pydantic import BaseModel
from typing import Literal

class AttendanceRequest(BaseModel):
    user_name: str
    type: Literal['checkin', 'checkout']

class HealthResponse(BaseModel):
    status: str
    database: str