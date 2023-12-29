from fastapi import APIRouter
from .model import LoginModel

router = APIRouter(
    tags=["Authentication"]
)

@router.post(path='/login')
def get_user(body: LoginModel):
    return {
        "email": body.email,
        "password": body.password 
    }