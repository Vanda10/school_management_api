from fastapi import APIRouter
from .model import LoginModel, RoleModel
from database.database import student_db, teacher_db, admin_db

router = APIRouter(
    tags=["Authentication"]
)

@router.post(path='/login')
def get_user(body: LoginModel):
    return {
        "email": body.email,
        "password": body.password 
    }

@router.get(path="/check_role")
def get_role(role: RoleModel, email: str):
    if role == RoleModel.Admin:
        is_exist = admin_db.find_one({"email": email})
        if is_exist: return True
        return False
    elif role == RoleModel.Studnet:
        is_exist = student_db.find_one({"email": email})
        if is_exist: return True
        return False
    elif role == RoleModel.Teacher:
        is_exist = teacher_db.find_one({"email": email})
        return False

    


