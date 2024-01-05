from pydantic import BaseModel

class Student(BaseModel):
    first_name: str
    last_name: str
    gender: str
    dob: str
    phone_number: str
    email: str
    password: str
    department_id: str
    class_id: str
    year: str

    class Config:
        orm_mode = True