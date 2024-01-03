from pydantic import BaseModel
from typing import TypeVar, Optional, Union

T = TypeVar('T')


class ResponseModel(BaseModel):
    data: Optional[Union[T, None]]
