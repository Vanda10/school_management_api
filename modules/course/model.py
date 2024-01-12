from pydantic import BaseModel

class Course(BaseModel):
    department_id: str
    coursename: str
    semester: str
    year: str

    class Config:
        orm_mode = True

