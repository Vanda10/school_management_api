from datetime import datetime
from pydantic import BaseModel

class Schedule(BaseModel):
    floor: str
    group_code: str
    classroom: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True