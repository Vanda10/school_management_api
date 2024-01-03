from pydantic import BaseModel

class Teacher(BaseModel):
    name: str
    specialist: str
    email: str
    password: int

    class Config:
        orm_mode = True
