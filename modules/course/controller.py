from fastapi import APIRouter, HTTPException
from database.database import course_db
from bson import ObjectId
from .model import Course

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)

# Get all courses with specific fields
    
# Get all courses with specific fields
@router.get("/")
def get_courses(department_id: str, semester: str, year: str):
    try:
        query = {"department_id": department_id, "semester": semester, "year": year}
        list_courses = list(course_db.find(query))
        for course in list_courses:
            if isinstance(course.get('_id'), ObjectId):
                course['id'] = str(course.pop('_id'))
        return {
            "data": list_courses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_all_course")
def get_all_courses():
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


# Create new course
@router.post("/")
def create_course(course: Course):
    try:
        new_course = course.dict()
        # Insert the new course into the database
        course_id = course_db.insert_one(new_course).inserted_id
        new_course['id'] = str(course_id)

        print("Add successfully")
        return {"data": f"Course with ID {new_course['id']} added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update course by ID
@router.put("/{department_id}/{semester}/{year}/{course_id}")
def update_course(department_id: str, semester: str, year: str, course_id: str, course: Course):
    updated_course = course.dict()
    if 'id' in updated_course:
        del updated_course['id']  # Ensure no 'id' is provided in the request body

    query = {"_id": ObjectId(course_id), "department_id": department_id, "semester": semester, "year": year}
    result = course_db.update_one(query, {"$set": updated_course})
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

# Update only coursename by ID
@router.patch("/{course_id}")
def update_course_coursename(course_id: str, coursename: str):
    try:
        query = {"_id": ObjectId(course_id)}
        result = course_db.update_one(query, {"$set": {"coursename": coursename}})
        
        if result.modified_count == 1:
            return {"data": f"Course with ID {course_id} updated successfully"}
        
        raise HTTPException(status_code=404, detail="Course not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
