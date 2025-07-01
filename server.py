from protocol import Protocol

class Server(Protocol):
    def __init__(self, server_info, options):
        super().__init__()
        self.capabilities = options.get('capabilities', {})
        self.instructions = options.get('instructions', '')
        self.server_info = server_info

        self.set_request_handler('initialize', self.oninitialize)
        self.set_notification_handler('notifications/initialized', self.oninitialized)

    async def oninitialize(self, request):
        params = request.params or {}
        self.capabilities.update(params.get('capabilities', {}))
        self.instructions = params.get('instructions', '')
        
        result = {
            'capabilities': self.capabilities,
            'serverInfo': self.server_info,
            'instructions': self.instructions
        }
        return result

    async def oninitialized(self, notification) -> None:
        pass