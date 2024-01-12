from fastapi import APIRouter, HTTPException
from database.database import department_db
from bson import ObjectId
from .model import Department

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)
@router.get("/")
def get_department_by_id(department_id: str):
    try:
        query = {"department_id": department_id}
        department = department_db.find_one(query)

        if department:
            # Assuming department has 'name' field, adjust accordingly
            department_name = department.get('name')
            department['_id'] = str(department.pop('_id'))  # Convert ObjectId to string if needed

            return {
                "data": {
                    "department_id": department_id,
                    "name": department_name
                }
            }
        else:
            return {
                "data": None,
                "message": f"Department with ID {department_id} not found."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

