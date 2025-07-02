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

    async def onerror(self, id, error) -> None:
        pass

    async def onmessage(self, message: dict) -> None:
        try:
            if "id" in message and "method" in message:
                await self.onrequest(message)
            elif "method" in message:
                await self.onnotification(message)
            elif "id" in message:
                await self.onresponse(message)
            else:
                id = message.get("id", None)
                error_response = {
                    "jsonrpc": "2.0",
                    "id": id,
                    "error": {"code": -32600, "message": "Invalid Request"},
                }
                self.transport.send(error_response)
        except Exception as e:
            id = message.get("id", None)
            error_response = {
                "jsonrpc": "2.0",
                "id": id,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
            }
            self.transport.send(error_response)

    async def onresponse(self, response) -> None:
        pass

    async def onrequest(self, request) -> None:
        method = request.get("method")
        id = request.get("id")
        handler = self.request_handlers.get(method)
        if not handler:
            error_response = {
                "jsonrpc": "2.0",
                "id": id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }
            self.transport.send(error_response)
            return

        try:
            result = await handler(request)
            response = {"jsonrpc": "2.0", "id": id, "result": result}
            self.transport.send(response)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            }
            self.transport.send(error_response)

    async def onnotification(self, notification) -> None:
        method = notification.get("method")
        handler = self.notification_handlers.get(method)
        if not handler:
            return
        await handler(notification)

    def set_request_handler(self, method: str, handler):
        self.request_handlers[method] = handler

    def set_notification_handler(self, method: str, handler):
        self.notification_handlers[method] = handler

    async def close(self) -> None:
        """プロトコル接続を閉じる"""
        if hasattr(self, "transport") and self.transport:
            self.transport.close()
