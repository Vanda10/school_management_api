from pydantic import BaseModel

class TeacherCourse(BaseModel):
    teacher_id: str
    group_code: str
    coursename: str
    
    class Config:
        orm_mode = True