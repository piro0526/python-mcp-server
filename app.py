import asyncio

from example_tools import add_tool, divide_tool, multiply_tool, subtract_tool
from mcp_server import MCPServer
from transport import stdio_transport


async def main():
    server_info = {
        "name": "ExampleServer",
        "title": "Example Server Display Name",
        "version": "1.0.0",
    }
    options = {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "instructions": "Optional instructions for the client",
    }
    mcp_server = MCPServer(server_info, options)
    mcp_server.set_tool_request_handler()

    mcp_server.register_tool(add_tool)
    mcp_server.register_tool(subtract_tool)
    mcp_server.register_tool(multiply_tool)
    mcp_server.register_tool(divide_tool)
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
