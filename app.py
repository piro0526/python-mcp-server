import asyncio
from transport import stdio_transport
from server import Server
from mcp import MCPServer
from mcp_types import Tool

async def main():
    server_info = {
        "name": "ExampleServer",
        "title": "Example Server Display Name",
        "version": "1.0.0"
    }
    options = {
        "capabilities": {
            "tools": {}
        },
        "instructions": "Optional instructions for the client"
    }
    mcp_server = MCPServer(server_info, options)
    mcp_server.set_tool_request_handler()
    
    example_tool = Tool(
        name="exampleTool",
        title="Example Tool",
        description="An example tool for demonstration purposes.",
        inputSchema={"type": "object", "properties": {"input": {"type": "string"}}},
        outputSchema={"type": "object", "properties": {"output": {"type": "string"}}},
        callback=lambda input: {"output": f"Processed input: {input['input']}"}
    )
    mcp_server.register_tool(example_tool)
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