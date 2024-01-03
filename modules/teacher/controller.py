from fastapi import APIRouter, HTTPException
from typing import List
from .model import Teacher
from database.database import teacher_db
from bson import ObjectId

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
)

# Get all teachers
@router.get("/")
def get_teachers():
    try:
        list_teachers = list(teacher_db.find())
        for teacher in list_teachers:
            if isinstance(teacher.get('_id'), ObjectId):
                teacher['id'] = str(teacher.pop('_id'))
        return {
            "data": list_teachers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get teacher by ID
@router.get("/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: str):
    try:
        if not ObjectId.is_valid(teacher_id):
            raise HTTPException(status_code=400, detail="Invalid teacher ID format")

        teacher = teacher_db.find_one({"_id": ObjectId(teacher_id)})
        if teacher:
            teacher['id'] = str(teacher.pop('_id'))
            return teacher
        raise HTTPException(status_code=404, detail="Teacher not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new teacher
@router.post("/{teacer_id}", response_model=Teacher)
def create_teacher(teacher: Teacher):
    new_teacher = teacher.dict()
    del new_teacher['id']  # Ensure no 'id' is provided in the request body
    teacher_id = teacher_db.insert_one(new_teacher).inserted_id
    new_teacher['id'] = str(teacher_id)
    return new_teacher

# Update teacher by ID
@router.put("/{teacer_id}", response_model=Teacher)
def update_teacher(teacher_id: str, teacher: Teacher):
    updated_teacher = teacher.dict()
    del updated_teacher['id']  # Ensure no 'id' is provided in the request body
    result = teacher_db.update_one({"_id": ObjectId(teacher_id)}, {"$set": updated_teacher})
    if result.modified_count == 1:
        updated_teacher['id'] = teacher_id
        return updated_teacher
    raise HTTPException(status_code=404, detail="Teacher not found")

# Delete teacher by ID
@router.delete("/{teacher_id}", response_model=Teacher)
def delete_teacher(teacher_id: str):
    teacher = teacher_db.find_one_and_delete({"_id": ObjectId(teacher_id)})
    if teacher:
        teacher['id'] = str(teacher.pop('_id'))
        return teacher
    raise HTTPException(status_code=404, detail="Teacher not found")

