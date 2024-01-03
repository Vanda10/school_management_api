from fastapi import APIRouter, HTTPException
from typing import List
from .model import Student
from database.database import student_db
import json
from bson import ObjectId

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

# Sample data file path
data_file = "module/student/student_data.json"

# Read data from file
def read_data():
    with open(data_file, "r") as file:
        return json.load(file)

# Write data to file
def write_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

# Get all students
@router.get("/")
def get_students():
    try:
        list_student = list(student_db.find())
        for student in list_student:
            if isinstance(student.get('_id'), ObjectId):
                student['id'] = str(student.pop('_id'))
        return {
            "data": list_student
        }
    except ValueError as e:
       raise HTTPException(status_code=500, detail=e)

# Get student by ID
@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):
    data = read_data()
    for student in data:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

# Create new student
@router.post("/", response_model=Student)
def create_student(student: Student):
    data = read_data()
    new_student = student.dict()
    new_student["id"] = len(data) + 1
    data.append(new_student)
    write_data(data)
    return new_student

# Update student by ID
@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    data = read_data()
    for s in data:
        if s["id"] == student_id:
            s.update(student.dict())
            write_data(data)
            return s
    raise HTTPException(status_code=404, detail="Student not found")

# Delete student by ID
@router.delete("/{student_id}", response_model=Student)
def delete_student(student_id: int):
    data = read_data()
    for index, s in enumerate(data):
        if s["id"] == student_id:
            del data[index]
            write_data(data)
            return s
    raise HTTPException(status_code=404, detail="Student not found")
