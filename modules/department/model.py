from pydantic import BaseModel

class Department(BaseModel):
    department_id: str
    name: str

    class Config:
        orm_mode = True