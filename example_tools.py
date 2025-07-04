from mcp_types import Tool

add_tool = Tool(
    definition={
        "name": "add_number",
        "title": "add_number",
        "description": "Adds two numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "int32"},
                "b": {"type": "int32"},
            },
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "output": {"type": "int32"},
            },
        },
    },
    callback=lambda **kwargs: {"output": kwargs.get("a", 0) + kwargs.get("b", 0)},
)

subtract_tool = Tool(
    definition={
        "name": "subtract_number",
        "title": "subtract_number",
        "description": "Subtracts two numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "int32"},
                "b": {"type": "int32"},
            },
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "output": {"type": "int32"},
            },
        },
    },
    callback=lambda **kwargs: {"output": kwargs.get("a", 0) - kwargs.get("b", 0)},
)

multiply_tool = Tool(
    definition={
        "name": "multiply_number",
        "title": "multiply_number",
        "description": "Multiplies two numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "int32"},
                "b": {"type": "int32"},
            },
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "output": {"type": "int32"},
            },
        },
    },
    callback=lambda **kwargs: {"output": kwargs.get("a", 0) * kwargs.get("b", 0)},
)

divide_tool = Tool(
    definition={
        "name": "divide_number",
        "title": "divide_number",
        "description": "Divides two numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "int32"},
                "b": {"type": "int32"},
            },
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "output": {"type": "float32"},
            },
        },
    },
    callback=lambda **kwargs: {"output": kwargs.get("a", 0) / kwargs.get("b", 1)},
)
