from server import Server
import json
import asyncio

class MCPServer():
    def __init__(self, server_info, options):
        self.server = Server(server_info, options)
        self.tools_list = {}


    async def connect(self, transport) -> None:
        await self.server.connect(transport)

    async def close(self) -> None:
        await self.server.close()
    
    def set_tool_request_handler(self) -> None:
        self.server.set_request_handler('tools/list', self.handle_tools_list)
        self.server.set_request_handler('tools/call', self.handle_call_tool)

    async def handle_tools_list(self, request) -> None:
        tool_definitions = [tool.definition for tool in self.tools_list.values()]
        result = {
            'tools': tool_definitions
        }
        return result

    async def handle_call_tool(self, request) -> None:
        params = request.params or {}
        tool_name = params.get('name', '')
        tool_params = params.get('arguments', {})

        if tool_name not in self.tools_list:
            error = {
                'code': -32601,
                'message': f'Tool "{tool_name}" not found.'
            }
            return error


        tool = self.tools_list[tool_name]

        # コールバックが非同期関数かどうかチェック
        if asyncio.iscoroutinefunction(tool.callback):
            output = await tool.callback(**tool_params)
        else:
            output = tool.callback(**tool_params)

        result = {
            'content': [
                {
                    'type': 'text',
                    'text': json.dumps(output)
                }
            ],
            'structuredContent': output
        }
        return result

    def register_tool(self, tool) -> None:
        if tool.name in self.tools_list:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        
        self.tools_list[tool.name] = tool