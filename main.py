from typing import Union
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from modules.login.controller import router as loginRouter
from modules.teacher.controller import router as TeacherRouter
from modules.student.controller import router as StudentRouter
from modules.course.controller import router as CourseRouter
from modules.classes.controller import router as ClassRouter
from modules.class_schedule.controller import router as schedule
from modules.department.controller import router as DepartmentRouter
from modules.teachercourse.controller import router as TeacherCourseRouter
from database.database import admin_db, student_db, teacher_db, url

app = FastAPI(docs_url='/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB settings
ADMIN_DB_NAME = 'admin_db'
STUDENTS_DB_NAME = 'student_db'
TEACHERS_DB_NAME = 'teacher_db'

# OAuth2 for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the MongoDB client
async def get_database(db_name: str):
    client = AsyncIOMotorClient(url)
    database = client[db_name]
    return database

# Authentication logic
async def authenticate_user(username: str, password: str, role: str, db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['users']

    user = await collection.find_one({"username": username, "password": password})

    return user is not None and user.get("role") == role

# Example usage
@app.post("/login")
async def login(username: str, password: str, role: str):
    db_name = None

    if role == 'admin':
        db_name = ADMIN_DB_NAME
    elif role == 'student':
        db_name = STUDENTS_DB_NAME
    elif role == 'teacher':
        db_name = TEACHERS_DB_NAME
    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    authenticated = await authenticate_user(username, password, role, await get_database(db_name))

    if authenticated:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
app.include_router(TeacherRouter)
app.include_router(StudentRouter)
app.include_router(CourseRouter)
app.include_router(ClassRouter)
app.include_router(schedule)
app.include_router(loginRouter)
app.include_router(DepartmentRouter)
app.include_router(TeacherCourseRouter)

if __name__ == "__main__":
    uvicorn.run(app=app)
