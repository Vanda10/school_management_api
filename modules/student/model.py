from pydantic import BaseModel

class Student(BaseModel):
    first_name: str
    last_name: str
    gender: str
    dob: str
    phone_number: str
    email: str
    department_id: str
    group_code: str

    class Config:
        orm_mode = True