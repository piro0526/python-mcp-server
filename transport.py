import sys

class transport:
    def __init__(self) -> None:
        pass

    def start(self) -> None:
        pass

    def send(self, message) -> None:
        pass

    def close(self) -> None:
        pass

    def onmessage(self, message) -> None:
        pass

    def onerror(self, error) -> None:
        pass

    def onclose(self) -> None:
        pass

class stdio_transport(transport):
    def __init__(self) -> None:
        super().__init__()

    def start(self) -> None:
        self.started = True
        self.

    def close(self) -> None:
        pass

    def onmessage(self, message) -> None:
        pass

    def onerror(self, error) -> None:
        pass

    def onclose(self) -> None:
        pass

    def 