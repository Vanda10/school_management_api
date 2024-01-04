from fastapi import APIRouter, HTTPException, status
from typing import List
from database.database import student_db
from database.response import ResponseModel
from bson import ObjectId
from .model import Student

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

# Get all students with specific fields
@router.get("/")
def get_students():
    try:
        # Retrieve data from the database, ensuring the correct field names
        list_students = list(student_db.find({}, {"_id": 1, "name": 1, "email": 1, "major": 1}))

        # Transform the data to match the response model
        formatted_students = [{"id": str(student["_id"]), "name": student.get("name", "N/A"), "email": student.get("email", "N/A"), "major": student.get("major", "N/A")} for student in list_students]

        return {
            "data": formatted_students
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get student by ID
@router.get("/{student_id}")
def get_student(student_id: str):
    try:
        if not ObjectId.is_valid(student_id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")
        
        student = student_db.find_one({"_id": ObjectId(student_id)})
        if student:
            student['id'] = str(student.pop('_id'))
            return student
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new student
@router.post("/")
def create_student(student: Student):
    try:
        new_student = student.dict()
        supbase_id = new_student.pop("id")
        # Remove the 'id' field if it exists in the request body
        if 'id' in new_student:
            del new_student['id']
        # Insert the new student into the database
        student_id = student_db.insert_one(new_student).inserted_id
        student_db.update_one({"_id": ObjectId(supbase_id)})
        new_student['id'] = str(student_id)

        print("Add successfully")
        return {"data": f"Student with ID {new_student['id']} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update student by ID
@router.put("/{student_id}")
def update_student(student_id: str, student: Student):
    updated_student = student.dict()
    if 'id' in updated_student:
        del updated_student['id']  # Ensure no 'id' is provided in the request body
    result = student_db.update_one({"_id": ObjectId(student_id)}, {"$set": updated_student})
    if result.modified_count == 1:
        updated_student['id'] = student_id
        return {"data": f"Student with ID {updated_student['id']} updated successfully"}
    raise HTTPException(status_code=404, detail="Student not found")

# Delete student by ID
@router.delete("/{student_id}")
def delete_student(student_id: str):
    student = student_db.find_one_and_delete({"_id": ObjectId(student_id)})
    if student:
        student['id'] = str(student.pop('_id'))
        print("Delete successful")
        return {"data": f"Student with ID {student_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
