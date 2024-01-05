from pydantic import BaseModel

class Class(BaseModel):
    classid: str
    classname: str

    class Config:
        orm_mode = True