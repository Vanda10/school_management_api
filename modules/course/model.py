from pydantic import BaseModel

class Course(BaseModel):
    name: str
    description: str
    teacher: str

    class Config:
        orm_mode = True