from pydantic import BaseModel

class Teacher(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
