from pydantic import BaseModel

class Teacher(BaseModel):
    name: str
    specialist: str
    email: str
    password: str

    class Config:
        orm_mode = True
