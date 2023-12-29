from typing import Union
import uvicorn
from fastapi import FastAPI
from modules.login.controller import router as loginRouter
from modules.teacher.controller import router as TeacherRouter
from fastapi.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    uvicorn.run(app=app)