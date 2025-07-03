import asyncio

from mcp_server import MCPServer
from mcp_types import Tool
from transport import http_transport
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


async def main():
    server_info = {"name": "ExampleServer", "title": "Example Server Display Name", "version": "1.0.0"}
    options = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "instructions": "Optional instructions for the client"}
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
    transport = http_transport()
    await mcp_server.connect(transport)

    class MCPHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message = post_data.decode('utf-8')
            transport.handle_request(message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')


if __name__ == "__main__":
    asyncio.run(main())