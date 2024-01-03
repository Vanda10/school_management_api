from pydantic import BaseModel

class Student(BaseModel):
    name: str
    major: str
    email: str
    password: int

    class Config:
        orm_mode = True