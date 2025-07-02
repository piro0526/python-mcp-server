import asyncio

from mcp import MCPServer
from mcp_types import Tool
from transport import stdio_transport


async def main():
    server_info = {"name": "ExampleServer", "title": "Example Server Display Name", "version": "1.0.0"}
    options = {"capabilities": {"tools": {}}, "instructions": "Optional instructions for the client"}
    mcp_server = MCPServer(server_info, options)
    mcp_server.set_tool_request_handler()

    add_tool = Tool(
        name="add_number",
        title="add_number",
        description="Adds two numbers.",
        inputSchema={"type": "object", "properties": {"a": {"type": "int32"}, "b": {"type": "int32"}}},
        outputSchema={"type": "object", "properties": {"output": {"type": "int32"}}},
        callback=lambda **kwargs: {"output": kwargs.get('a', 0) + kwargs.get('b', 0)},
    )
    mcp_server.register_tool(add_tool)
    transport = stdio_transport()
    await mcp_server.connect(transport)

    # サーバーを永続的に実行
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await mcp_server.close()


if __name__ == "__main__":
    asyncio.run(main())
