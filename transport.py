import asyncio
import json
import sys
from typing import Callable, Dict, Optional


class transport:
    def __init__(self) -> None:
        self.onmessage: Optional[Callable] = None
        self.onerror: Optional[Callable] = None
        self.onclose: Optional[Callable] = None

    def start(self) -> None:
        pass

    def send(self, message) -> None:
        pass

    def close(self) -> None:
        pass


class stdio_transport(transport):
    def __init__(self) -> None:
        super().__init__()
        self.started = False
        self.closed = False
        self.onmessage: Optional[Callable] = None
        self.onerror: Optional[Callable] = None
        self.onclose: Optional[Callable] = None

    def start(self) -> None:
        if self.started:
            return

        self.started = True
        # stdin からメッセージを非同期で読み取り開始
        asyncio.create_task(self._read_messages())

    async def _read_messages(self) -> None:
        """標準入力からJSON-RPC メッセージを読み取る"""
        try:
            while not self.closed:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

                line = line.strip()

                try:
                    message = json.loads(line)
                    if self.onmessage:
                        await self.onmessage(message)
                except json.JSONDecodeError as e:
                    if self.onerror:
                        continue

        except Exception as e:
            if self.onerror:
                return
        finally:
            if self.onclose:
                self.onclose()

    def send(self, message: Dict) -> None:
        """メッセージを標準出力に送信"""
        if self.closed:
            return
        try:
            json_message = json.dumps(message, ensure_ascii=False)
            print(json_message, flush=True)
        except Exception as e:
            if self.onerror:
                return

    def close(self) -> None:
        """トランスポートを閉じる"""
        self.closed = True
        self.started = False


class http_transport(transport):
    def __init__(self) -> None:
        super().__init__()
        self.session = None

    def start(self) -> None:
        pass

    async def handle_request(self, request_json) -> None:
        """HTTPリクエストを処理する"""
        request = json.loads(request_json)
        if self.onmessage:
            await self.onmessage(request)

    def send(self, message) -> None:
        pass

    def close(self) -> None:
        pass
