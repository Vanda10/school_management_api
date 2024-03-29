from pydantic import BaseModel

class Class(BaseModel):
    group_code: str
    department_id: str
    semester: str
    year: str

    class Config:
        orm_mode = True