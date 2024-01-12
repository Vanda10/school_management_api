from fastapi import APIRouter, HTTPException
from database.database import schedule_db
from bson import ObjectId
from .model import Schedule  # Update the import to use Schedule instead of Class
from typing import List


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
    
# Get class schedules by floor
@router.get("/{floor}", response_model=List[Schedule])  # Add this endpoint
def get_class_schedules_by_floor(floor: str):
    try:
        # Filter schedules by floor
        list_class_schedules = list(schedule_db.find({"floor": floor}))
        
        # Convert ObjectId to string for response
        for class_schedule_obj in list_class_schedules:
            if isinstance(class_schedule_obj.get('_id'), ObjectId):
                class_schedule_obj['id'] = str(class_schedule_obj.pop('_id'))

        return list_class_schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add class schedule by floor
@router.post("/{floor}", response_model=Schedule)  # Add this endpoint
def add_class_schedule(floor: str, schedule: Schedule):
    try:
        # Set the floor for the schedule
        schedule.floor = floor
        
        # Insert the schedule into the database
        result = schedule_db.insert_one(schedule.dict())
        
        # Retrieve the inserted schedule
        inserted_schedule = schedule_db.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string for response
        if isinstance(inserted_schedule.get('_id'), ObjectId):
            inserted_schedule['id'] = str(inserted_schedule.pop('_id'))
        
        return inserted_schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
