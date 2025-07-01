from mcp_types import Error, Request, Response, Notification

class Protocol:
    def __init__(self):
        # self.response_handlers = {}
        self.request_handlers = {}
        self.notification_handlers = {}

    async def connect(self, transport):
        self.transport = transport
        self.transport.onclose = self.onclose
        self.transport.onerror = self.onerror
        self.transport.onmessage = self.onmessage

        self.transport.start()

    def onclose(self) -> None:
        pass

    async def onerror(self, error: Error) -> None:
        pass

    async def onmessage(self, message) -> None:
        # 辞書からPydanticモデルに変換
        try:
            if "id" in message and "method" in message:
                request = Request(**message)
                await self.onrequest(request)
            elif "method" in message:
                notification = Notification(**message)
                await self.onnotification(notification)
            elif "id" in message:
                response = Response(**message)
                await self.onresponse(response)
            else:
                await self.onerror(Error(code=-32600, message=f"Invalid message format: {message}"))
        except Exception as e:
            await self.onerror(Error(code=-32700, message=f"Parse error: {e}"))

    async def onresponse(self, response: Response) -> None:
        pass

    async def onrequest(self, request: Request) -> None:
        handler = self.request_handlers.get(request.method)
        if not handler:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {request.method}"
                }
            }
            self.transport.send(error_response)
            return

        try:
            result = await handler(request)
            response = {
                "jsonrpc": "2.0",
                "id": request.id,
                "result": result
            }
            self.transport.send(response)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            self.transport.send(error_response)

    async def onnotification(self, notification: Notification) -> None:
        handler = self.notification_handlers.get(notification.method)
        if not handler:
            await self.onerror(Error(code=-32601, message=f"No handler for notification method: {notification.method}"))
            return
        
        try:
            await handler(notification)
        except Exception as e:
            await self.onerror(Error(code=-32603, message=f"Error handling notification: {str(e)}"))
    
    def set_request_handler(self, method: str, handler: callable):
        if method in self.request_handlers:
            raise Error(f"Request handler for method '{method}' already exists.")
        self.request_handlers[method] = handler

    def set_notification_handler(self, method: str, handler: callable):
        if method in self.notification_handlers:
            raise Error(f"Notification handler for method '{method}' already exists.")
        self.notification_handlers[method] = handler
    
    async def close(self) -> None:
        """プロトコル接続を閉じる"""
        if hasattr(self, 'transport') and self.transport:
            self.transport.close()