from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

class Request(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: str
    params: Optional[Dict[str, Any]] = None

class Result(BaseModel):
    pass

class Notification(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None

class Error(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

class Response(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    result: Optional[Any] = None
    error: Optional[Error] = None

class Tool:
    def __init__(self, name: str, title: str, description: str,
                 inputSchema: Dict[str, Any], outputSchema: Dict[str, Any],
                 callback: callable):
        self.name = name
        self.title = title
        self.description = description
        self.inputSchema = inputSchema
        self.outputSchema = outputSchema
        self.callback = callback
    
    @property
    def definition(self) -> Dict[str, Any]:
        """ツールの定義をMCP形式で返す"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.inputSchema
        }