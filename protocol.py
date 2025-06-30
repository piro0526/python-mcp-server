from types import Error, Request, Response, Notification

class Protocol:
    def __init__(self, name, version):
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

    def onerror(self, error: Error) -> None:
        pass

    def onmessage(self, message) -> None:
        if isinstance(message, Response):
            self.onresponse(message)
        elif isinstance(message, Request):
            self.onrequest(message)
        elif isinstance(message, Notification):
            self.onnotification(message)
        else:
            self.onerror(Error(f"Unknown message type: {type(message)}"))

    def onresponse(self, response: Response) -> None:
        pass

    def onrequest(self, request: Request) -> None:
        handler = self.request_handlers.get(request.method)
        if handler:
            handler(request)
        else:
            self.onerror(Error(f"No handler for request method: {request.method}"))

    def onnotification(self, notification: Notification) -> None:
        handler = self.notification_handlers.get(notification.method)
        if handler:
            handler(notification)
        else:
            self.onerror(Error(f"No handler for notification method: {notification.method}"))
    
    def set_request_handler(self, method: str, handler: callable):
        if method in self.request_handlers:
            raise Error(f"Request handler for method '{method}' already exists.")
        self.request_handlers[method] = handler

    def set_notification_handler(self, method: str, handler: callable):
        if method in self.notification_handlers:
            raise Error(f"Notification handler for method '{method}' already exists.")
        self.notification_handlers[method] = handler