from fastapi import APIRouter, HTTPException, status
from typing import List
from .model import Teacher
from database.database import teacher_db
from database.response import ResponseModel
from bson import ObjectId
from typing import List, Dict, Any

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
)

# # Get all teachers
# @router.get("/")
# def get_teachers():
#     try:
#         list_teachers = list(teacher_db.find())
#         for teacher in list_teachers:
#             if isinstance(teacher.get('_id'), ObjectId):
#                 teacher['id'] = str(teacher.pop('_id'))
#         return {
#             "data": list_teachers
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Get all teachers with specific fields
@router.get("/")
def get_teachers():
    try:
        # Retrieve data from the database, ensuring the correct field names
        list_teachers = list(teacher_db.find({}, {"_id": 1, "name": 1, "email": 1}))

        # Transform the data to match the response model
        formatted_teachers = [{"id": str(teacher["_id"]), "name": teacher.get("name", "N/A"), "email": teacher.get("email", "N/A")} for teacher in list_teachers]

        return {
            "data": formatted_teachers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get teacher by ID
@router.get("/{teacher_id}")
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
@router.post("/")
def create_teacher(teacher: Teacher):
    try:
        new_teacher = teacher.dict()
        # Remove the 'id' field if it exists in the request body
        if 'id' in new_teacher:
            del new_teacher['id']
        # Insert the new teacher into the database
        teacher_id = teacher_db.insert_one(new_teacher).inserted_id
        new_teacher['id'] = str(teacher_id)

        print("Add successfully")
        return {"data": f"Teacher with ID {new_teacher['id']} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update teacher by ID
@router.put("/{teacher_id}")
def update_teacher(teacher_id: str, teacher: Teacher):
    updated_teacher = teacher.dict()
    if 'id' in updated_teacher:
        del updated_teacher['id']  # Ensure no 'id' is provided in the request body
    result = teacher_db.update_one({"_id": ObjectId(teacher_id)}, {"$set": updated_teacher})
    if result.modified_count == 1:
        updated_teacher['id'] = teacher_id
        return {"data": f"Teacher with ID {updated_teacher['id']} updated successfully"}
    raise HTTPException(status_code=404, detail="Teacher not found")


# Delete teacher by ID
@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: str):
    teacher = teacher_db.find_one_and_delete({"_id": ObjectId(teacher_id)})
    if teacher:
        teacher['id'] = str(teacher.pop('_id'))
        print("Delete successful")
        return {"data": f"Teacher with ID {teacher_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Teacher not found")

