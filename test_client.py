#!/usr/bin/env python3
"""
MCPサーバーテスト用クライアント
サーバーと直接通信してテストを実行します
"""

import asyncio
import json
import sys
from typing import Any, Dict


class MCPTestClient:
    def __init__(self):
        self.process = None
        self.message_id = 0

    async def start_server(self):
        """MCPサーバーを起動"""
        print("🚀 MCPサーバーを起動中...")
        self.process = await asyncio.create_subprocess_exec(
            sys.executable,
            "app.py",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        print(f"✅ サーバーが起動しました (PID: {self.process.pid})")

    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """メッセージを送信してレスポンスを受信"""
        if not self.process:
            raise RuntimeError("サーバーが起動していません")

        # メッセージを JSON として送信
        message_str = json.dumps(message) + "\n"
        print(f"📤 送信: {message_str.strip()}")

        self.process.stdin.write(message_str.encode())
        await self.process.stdin.drain()

        # レスポンスを受信
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("サーバーからレスポンスがありません")

        try:
            response = json.loads(response_line.decode().strip())
            print(f"📥 受信: {json.dumps(response, indent=2, ensure_ascii=False)}")
            return response
        except json.JSONDecodeError as e:
            print(f"❌ JSONデコードエラー: {e}")
            print(f"生データ: {response_line.decode().strip()}")
            return {}

    def next_id(self) -> int:
        """次のメッセージIDを取得"""
        self.message_id += 1
        return self.message_id

    async def test_initialize(self):
        """初期化テスト"""
        print("\n🔧 テスト1: サーバー初期化")
        message = {
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }
        return await self.send_message(message)

    async def test_tools_list(self):
        """ツールリストテスト"""
        print("\n📋 テスト2: ツールリスト取得")
        message = {"jsonrpc": "2.0", "id": self.next_id(), "method": "tools/list", "params": {}}
        return await self.send_message(message)

    async def test_tool_call(self, input_text: str = "Hello, MCP!"):
        """ツール実行テスト"""
        print(f"\n🔧 テスト3: ツール実行 (入力: {input_text})")
        message = {
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": "tools/call",
            "params": {"name": "exampleTool", "arguments": {"input": input_text}},
        }
        return await self.send_message(message)

    async def test_invalid_tool(self):
        """存在しないツール実行テスト"""
        print("\n❌ テスト4: 存在しないツール実行（エラーテスト）")
        message = {
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": "tools/call",
            "params": {"name": "nonExistentTool", "arguments": {}},
        }
        return await self.send_message(message)

    async def stop_server(self):
        """サーバーを停止"""
        if self.process:
            print("\n🛑 サーバーを停止中...")
            self.process.terminate()
            await self.process.wait()
            print("✅ サーバーが停止しました")


async def main():
    """メインテスト実行"""
    client = MCPTestClient()

    try:
        # サーバー起動
        await client.start_server()
        await asyncio.sleep(1)  # 起動待機

        # テスト実行
        await client.test_initialize()
        await client.test_tools_list()
        await client.test_tool_call("テストメッセージです")
        await client.test_invalid_tool()

        print("\n✅ 全テストが完了しました！")

    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生しました: {e}")
    finally:
        await client.stop_server()


if __name__ == "__main__":
    asyncio.run(main())
