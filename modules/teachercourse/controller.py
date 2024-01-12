from fastapi import APIRouter, HTTPException
from database.database import teacherCourse_db
from bson import ObjectId
from .model import TeacherCourse

router = APIRouter(
    prefix="/teacher-courses",
    tags=["Teacher Courses"],
)

# Get teacher courses by teacher_id
@router.get("/{teacher_id}")
def get_teacher_courses(teacher_id: str):
    try:
        query = {"teacher_id": teacher_id}
        teacher_courses = list(teacherCourse_db.find(query))
        for course in teacher_courses:
            if isinstance(course.get('_id'), ObjectId):
                course['id'] = str(course.pop('_id'))
        return {
            "data": teacher_courses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Get all teacher courses
@router.get("/")
def get_all_teacher_courses():
    try:
        teacher_courses = list(teacherCourse_db.find())
        for course in teacher_courses:
            if isinstance(course.get('_id'), ObjectId):
                course['id'] = str(course.pop('_id'))
        return {
            "data": teacher_courses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update teacher course by object_id
@router.put("/{object_id}")
def update_teacher_course(object_id: str, teacher_course: TeacherCourse):
    try:
        # Convert the object_id and teacher_id to ObjectId if needed
        object_id = ObjectId(object_id)
        teacher_id = str(teacher_course.teacher_id)  # Assuming teacher_id is not a string

        # Update the record
        teacherCourse_db.update_one(
            {"_id": object_id, "teacher_id": teacher_id},
            {"$set": teacher_course.dict(exclude={"teacher_id"})}
        )
        return {"message": "Record updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete teacher course by object_id
@router.delete("/{object_id}")
def delete_teacher_course(object_id: str):
    try:
        # Convert the object_id to ObjectId
        object_id = ObjectId(object_id)

        # Delete the record
        result = teacherCourse_db.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add new record to teacherCourse_db
@router.post("/")
def add_teacher_course(teacher_course: TeacherCourse):
    try:
        # Convert the teacher_id to string if needed
        teacher_id = str(teacher_course.teacher_id)  # Assuming teacher_id is not a string

        # Add a new record
        result = teacherCourse_db.insert_one(teacher_course.dict())
        inserted_id = str(result.inserted_id)
        return {"message": "Record added successfully", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
