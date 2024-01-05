from fastapi import APIRouter, HTTPException
from database.database import schedule_db
from bson import ObjectId
from .model import Schedule  # Update the import to use Schedule instead of Class

router = APIRouter(
    prefix="/schedule",  # Change the prefix to /classes instead of /courses
    tags=["Schedule"],   # Change the tag to Classes instead of Courses
)

# Get all class_schedules with specific fields
@router.get("/")
def get_class_schedules():
    try:
        list_class_schedules = list( schedule_db.find())  # Update variable names to list_class_schedules
        for class_schedule_obj in list_class_schedules:  # Update variable names to class_schedule_obj
            if isinstance(class_schedule_obj.get('_id'), ObjectId):
                class_schedule_obj['id'] = str(class_schedule_obj.pop('_id'))
        return {
            "data": list_class_schedules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get class_schedule by ID
@router.get("/{class_schedule_id}")
def get_class_schedule(class_schedule_id: str):  # Update parameter names to use class_schedule_id
    try:
        if not ObjectId.is_valid(class_schedule_id):  # Update variable names to class_schedule_id
            raise HTTPException(status_code=400, detail="Invalid class_schedule ID format")  # Update variable names to class_schedule ID

        class_schedule_obj =  schedule_db.find_one({"_id": ObjectId(class_schedule_id)})  # Update variable names to class_schedule_obj
        if class_schedule_obj:
            class_schedule_obj['id'] = str(class_schedule_obj.pop('_id'))
            return class_schedule_obj
        raise HTTPException(status_code=404, detail="Class_schedule not found")  # Update detail message to Class_schedule not found
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new class_schedule
@router.post("/")
def create_class_schedule(class_schedule_obj: Schedule):  # Update parameter names to class_schedule_obj and use Schedule model
    try:
        new_class_schedule = class_schedule_obj.dict()  # Update variable names to new_class_schedule
        # Remove the 'id' field if it exists in the request body
        if 'id' in new_class_schedule:
            del new_class_schedule['id']
        # Insert the new class_schedule into the database
        class_schedule_id =  schedule_db.insert_one(new_class_schedule).inserted_id
        new_class_schedule['id'] = str(class_schedule_id)

        print("Add successfully")
        return {"data": f"Class_schedule with ID {new_class_schedule['id']} added successfully"}  # Update message to Class_schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update class_schedule by ID
@router.put("/{class_schedule_id}")
def update_class_schedule(class_schedule_id: str, class_schedule_obj: Schedule):  # Update parameter names to class_schedule_id and class_schedule_obj
    updated_class_schedule = class_schedule_obj.dict()  # Update variable names to updated_class_schedule
    if 'id' in updated_class_schedule:
        del updated_class_schedule['id']  # Ensure no 'id' is provided in the request body
    result =  schedule_db.update_one({"_id": ObjectId(class_schedule_id)}, {"$set": updated_class_schedule})  # Update variable names
    if result.modified_count == 1:
        updated_class_schedule['id'] = class_schedule_id
        return {"data": f"Class_schedule with ID {updated_class_schedule['id']} updated successfully"}  # Update message to Class_schedule
    raise HTTPException(status_code=404, detail="Class_schedule not found")  # Update detail message to Class_schedule not found

# Delete class_schedule by ID
@router.delete("/{class_schedule_id}")
def delete_class_schedule(class_schedule_id: str):  # Update parameter name to class_schedule_id
    class_schedule_id = class_schedule_id.strip()  # Strip leading and trailing whitespace
    if not ObjectId.is_valid(class_schedule_id):
        raise HTTPException(status_code=400, detail="Invalid class_schedule ID format")

    class_schedule_obj = schedule_db.find_one_and_delete({"_id": ObjectId(class_schedule_id)})

    if class_schedule_obj:
        class_schedule_obj['id'] = str(class_schedule_obj.pop('_id'))
        print("Delete successful")
        return {"data": f"Class_schedule with ID {class_schedule_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Class_schedule not found")
