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

    async def onerror(self, error) -> None:
        pass

    async def onmessage(self, message) -> None:
        # 辞書からPydanticモデルに変換
        print(f"DEBUG: Received message: {message}")
        try:
            if "id" in message and "method" in message:
                print(f"Received request: {message}")
                await self.onrequest(message)
            elif "method" in message:
                print(f"Received notification: {message}")
                await self.onnotification(message)
            elif "id" in message:
                print(f"Received response: {message}")
                await self.onresponse(message)
            else:
                print(f"Invalid message format: {message}")
                await self.onerror({"code": -32600, "message": "Invalid request format"})
        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback

            traceback.print_exc()
            await self.onerror({"code": -32700, "message": f"Parse error: {e}"})

    async def onresponse(self, response) -> None:
        pass

    async def onrequest(self, request) -> None:
        method = request.get("method")
        print(f"Processing request for method: {method}")
        print(f"Available request handlers: {list(self.request_handlers.keys())}")
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
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }
            self.transport.send(error_response)
            return
        await handler(notification)

    def set_request_handler(self, method: str, handler):
        if method in self.request_handlers:
            # raise Error(f"Request handler for method '{method}' already exists.")
            return
        print(f"Registering request handler for method: {method}")
        self.request_handlers[method] = handler

    def set_notification_handler(self, method: str, handler):
        if method in self.notification_handlers:
            # raise Error(f"Notification handler for method '{method}' already exists.")
            return
        print(f"Registering notification handler for method: {method}")
        self.notification_handlers[method] = handler

    async def close(self) -> None:
        """プロトコル接続を閉じる"""
        if hasattr(self, "transport") and self.transport:
            self.transport.close()
