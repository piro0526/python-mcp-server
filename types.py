from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Request(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = None

class Result(BaseModel):

class Notification(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = None

class Error(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

class Response(BaseModel):
    id: Optional[Union[str, int]] = None
    result: Optional[Result] = None
    error: Optional[Error] = None

class initialize