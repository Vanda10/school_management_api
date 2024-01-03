from pydantic import BaseModel
from typing import TypeVar, Optional

T = TypeVar('T')

class ResponseModel(BaseModel):
    data: Optional[T] | None