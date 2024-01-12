from fastapi import APIRouter, HTTPException
from .model import LoginModel, RoleModel
from database.database import student_db, teacher_db, admin_db
from bson import ObjectId

router = APIRouter(
    tags=["Authentication"]
)
@router.get(path="/check_role")
def get_role(role: RoleModel, email: str):
    if role == RoleModel.Admin:
        is_exist = admin_db.find_one({"email": email})
        if is_exist: 
            return True
        return False
    elif role == RoleModel.Studnet:  # Fix the typo here
        is_exist = student_db.find_one({"email": email})
        if is_exist: 
            return True
        return False
    elif role == RoleModel.Teacher:
        is_exist = teacher_db.find_one({"email": email})
        if is_exist: 
            return True
        return False
    else:
        return False

@router.get("/get_user_data")
def get_user_data(email: str, role: RoleModel):
    if role == RoleModel.Admin:
        user_data = admin_db.find_one({"email": email})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return user_data
        return False
    elif role == RoleModel.Studnet:  # Fix the typo here
        user_data = student_db.find_one({"email": email})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return user_data
        return False
    elif role == RoleModel.Teacher:
        user_data = teacher_db.find_one({"email": email})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return user_data
        return False
    else:
        return False
