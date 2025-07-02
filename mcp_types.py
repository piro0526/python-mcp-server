from typing import Any, Callable, Dict

'''
def isresponse(message: Dict[str, Any]) -> bool:
    """メッセージがレスポンスかどうかを判定"""
    return "id" in message and "result" in message


def isnotification(message: Dict[str, Any]) -> bool:
    """メッセージが通知かどうかを判定"""
    return "method" in message and "params" in message


def isrequest(message: Dict[str, Any]) -> bool:
    """メッセージがリクエストかどうかを判定"""
    return "method" in message and "id" in message


def iserror(message: Dict[str, Any]) -> bool:
    """メッセージがエラーかどうかを判定"""
    return "error" in message and "id" in message
'''


class Tool:
    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        inputSchema: Dict[str, Any],
        outputSchema: Dict[str, Any],
        callback: Callable,
    ):
        self.name = name
        self.title = title
        self.description = description
        self.inputSchema = inputSchema
        self.outputSchema = outputSchema
        self.callback = callback

    @property
    def definition(self) -> Dict[str, Any]:
        """ツールの定義をMCP形式で返す"""
        return {"name": self.name, "description": self.description, "inputSchema": self.inputSchema}
