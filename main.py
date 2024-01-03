from typing import Union
import uvicorn
from fastapi import FastAPI
from modules.login.controller import router as loginRouter
from modules.teacher.controller import router as TeacherRouter
from modules.student.controller import router as StudentRouter
from modules.course.controller import router as CourseRouter
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI(
    docs_url='/'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loginRouter)
app.include_router(TeacherRouter)
app.include_router(StudentRouter)
app.include_router(CourseRouter)

if __name__ == "__main__":
    uvicorn.run(app=app)