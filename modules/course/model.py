from pydantic import BaseModel

class Course(BaseModel):
    courseid: str
    coursename: str

    class Config:
        orm_mode = True