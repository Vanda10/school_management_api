from fastapi import APIRouter, HTTPException, Path
from database.database import classes_db
from bson import ObjectId
from modules.classes.model import Class  # Change the import to use Class instead of Course

router = APIRouter(
    prefix="/classes",  # Change the prefix to /classes instead of /courses
    tags=["Classes"],   # Change the tag to Classes instead of Courses
)

# Get all classes with specific fields
@router.get("/")
def get_classes():
    try:
        list_classes = list(classes_db.find())  # Update variable names to list_classes
        for class_obj in list_classes:  # Update variable names to class_obj
            if isinstance(class_obj.get('_id'), ObjectId):
                class_obj['id'] = str(class_obj.pop('_id'))
        return {
            "data": list_classes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get class by ID
@router.get("/{class_id}")
def get_class(class_id: str):  # Update parameter names to use class_id
    try:
        if not ObjectId.is_valid(class_id):  # Update variable names to class_id
            raise HTTPException(status_code=400, detail="Invalid class ID format")  # Update variable names to class ID

        class_obj = classes_db.find_one({"_id": ObjectId(class_id)})  # Update variable names to class_obj
        if class_obj:
            class_obj['id'] = str(class_obj.pop('_id'))
            return class_obj
        raise HTTPException(status_code=404, detail="Class not found")  # Update detail message to Class not found
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new class
@router.post("/")
def create_class(class_obj: Class):  # Update parameter names to class_obj and use Class model
    try:
        new_class = class_obj.dict()  # Update variable names to new_class
        # Remove the 'id' field if it exists in the request body
        if 'id' in new_class:
            del new_class['id']
        # Insert the new class into the database
        class_id = classes_db.insert_one(new_class).inserted_id
        new_class['id'] = str(class_id)

        print("Add successfully")
        return {"data": f"Class with ID {new_class['id']} added successfully"}  # Update message to Class
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update class by ID
@router.put("/{class_id}")
def update_class(class_id: str, class_obj: Class):  # Update parameter names to class_id and class_obj
    updated_class = class_obj.dict()  # Update variable names to updated_class
    if 'id' in updated_class:
        del updated_class['id']  # Ensure no 'id' is provided in the request body
    result = classes_db.update_one({"_id": ObjectId(class_id)}, {"$set": updated_class})  # Update variable names
    if result.modified_count == 1:
        updated_class['id'] = class_id
        return {"data": f"Class with ID {updated_class['id']} updated successfully"}  # Update message to Class
    raise HTTPException(status_code=404, detail="Class not found")  # Update detail message to Class not found

# Delete class by ID
@router.delete("/{class_id}")
def delete_class(class_id: str):  # Update parameter name to class_id
    class_obj = classes_db.find_one_and_delete({"_id": ObjectId(class_id)})  # Update variable names to class_obj
    if class_obj:
        class_obj['id'] = str(class_obj.pop('_id'))
        print("Delete successful")
        return {"data": f"Class with ID {class_id} deleted successfully"}  # Update message to Class
    raise HTTPException(status_code=404, detail="Class not found")  # Update detail message to Class not found

# Get class by group_code
@router.get("/group/{group_code}")
def get_class_by_group_code(group_code: str = Path(..., title="The group code of the class")):
    try:
        class_obj = classes_db.find_one({"group_code": group_code})
        if class_obj:
            class_obj['id'] = str(class_obj.pop('_id'))
            return class_obj
        raise HTTPException(status_code=404, detail="Class not found for the given group code")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update only semester and year of class by ID
@router.put("/{class_id}/update-semester-year")
def update_class_semester_year(class_id: str, semester: str, year: str):  # Update parameter names to class_id, semester, and year
    try:
        result = classes_db.update_one(
            {"_id": ObjectId(class_id)},
            {"$set": {"semester": semester, "year": year}}  # Update fields to be updated
        )
        if result.modified_count == 1:
            return {"data": f"Semester and year of class with ID {class_id} updated successfully"}
        raise HTTPException(status_code=404, detail="Class not found")  # Update detail message to Class not found
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


