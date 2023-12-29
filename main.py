from typing import Union
import uvicorn
from fastapi import FastAPI
from modules.login.controller import router as loginRouter
from modules.teacher.controller import router as TeacherRouter

app = FastAPI(
    docs_url='/'
)

app.include_router(loginRouter)
app.include_router(TeacherRouter)

if __name__ == "__main__":
    uvicorn.run(app=app)