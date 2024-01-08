from pydantic import BaseModel
from enum import Enum

class LoginModel(BaseModel):
    email: str
    password: str


class RoleModel(Enum):
    Studnet = "student"
    Teacher = "teacher"
    Admin = "admin"