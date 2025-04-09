# File: main.py

import sys
import asyncio
import logging
import json

from mcp.server.core import MCPServer
from mcp.server.stdio import StdioServerTransport
from mongodb.client import connect_to_mongodb, close_mongodb
from tools.registry import tool_registry

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def list_tools_handler():
    return {
        "tools": tool_registry.get_tool_schemas(),
        "_meta": {}
    }

async def call_tool_handler(params):
    name = params.get("name")
    args = params.get("arguments", {})
    try:
        logger.error(f"Executing tool: {name}")
        logger.error(f"Arguments: {json.dumps(args, indent=2)}")
        tool = tool_registry.get_tool(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")
        result = await tool.execute(args)
        return {"toolResult": result}
    except Exception as error:
        logger.error(f"Operation failed: {str(error)}")
        return {
            "toolResult": {
                "content": [{"type": "text", "text": str(error)}],
                "isError": True
            }
        }

async def run():
    if len(sys.argv) < 2:
        print("Please provide a MongoDB connection URL", file=sys.stderr)
        sys.exit(1)

    database_url = sys.argv[1]
    await connect_to_mongodb(database_url)

    server = MCPServer(name="mongodb-mcp", version="0.1.0")
    server.set_handler("list_tools", list_tools_handler)
    server.set_handler("call_tool", call_tool_handler)

    transport = StdioServerTransport()
    await server.connect(transport)
    logger.error("MongoDB MCP server running on stdio")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        asyncio.run(close_mongodb())
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        sys.exit(1)
