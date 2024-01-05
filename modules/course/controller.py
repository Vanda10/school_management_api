from fastapi import APIRouter, HTTPException
from database.database import course_db
from bson import ObjectId
from .model import Course

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)

# Get all courses with specific fields
@router.get("/")
def get_courses():
    try:
        list_courses = list(course_db.find())
        for course in list_courses:
            if isinstance(course.get('_id'), ObjectId):
                course['id'] = str(course.pop('_id'))
        return {
            "data": list_courses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get course by ID
@router.get("/{course_id}")
def get_course(course_id: str):
    try:
        if not ObjectId.is_valid(course_id):
            raise HTTPException(status_code=400, detail="Invalid course ID format")
        
        course = course_db.find_one({"_id": ObjectId(course_id)})
        if course:
            course['id'] = str(course.pop('_id'))
            return course
        raise HTTPException(status_code=404, detail="Course not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new course
@router.post("/")
def create_course(course: Course):
    try:
        new_course = course.dict()
        # Remove the 'id' field if it exists in the request body
        if 'id' in new_course:
            del new_course['id']
        # Insert the new course into the database
        course_id = course_db.insert_one(new_course).inserted_id
        new_course['id'] = str(course_id)

        print("Add successfully")
        return {"data": f"Course with ID {new_course['id']} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update course by ID
@router.put("/{course_id}")
def update_course(course_id: str, course: Course):
    updated_course = course.dict()
    if 'id' in updated_course:
        del updated_course['id']  # Ensure no 'id' is provided in the request body
    result = course_db.update_one({"_id": ObjectId(course_id)}, {"$set": updated_course})
    if result.modified_count == 1:
        updated_course['id'] = course_id
        return {"data": f"Course with ID {updated_course['id']} updated successfully"}
    raise HTTPException(status_code=404, detail="Course not found")

# Delete course by ID
@router.delete("/{course_id}")
def delete_course(course_id: str):
    course = course_db.find_one_and_delete({"_id": ObjectId(course_id)})
    if course:
        course['id'] = str(course.pop('_id'))
        print("Delete successful")
        return {"data": f"Course with ID {course_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Course not found")
