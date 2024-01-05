from pydantic import BaseModel

class Schedule(BaseModel):
    classid: str
    date:str
    start_time:str
    end_time:str

    class Config:
        orm_mode = True