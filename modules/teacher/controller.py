from fastapi import APIRouter
import json

router = APIRouter(
    tags=["Teacher"]
)

@router.get(path='/get_teacher')
def get():
    with open('/Users/mac/Desktop/school_management_api/data/teacher.json', 'r') as f:
        data = f.read()
        data = json.loads(data)

    return {
        "data": data
    }