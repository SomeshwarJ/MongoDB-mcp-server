# File: tools/create_index_tool.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def createIndex(collection: str, indexSpec: dict) -> dict:
    """
    Create a new index on a MongoDB collection.

    Args:
        collection: Name of the collection
        indexSpec: Index specification (e.g., { field: 1 } for ascending index)

    Returns:
        A dictionary with the name of the created index.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")
        if not isinstance(indexSpec, dict):
            raise ValueError("indexSpec must be a dictionary")

        index_name = await db[collection].create_index(indexSpec)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"indexName": index_name}, indent=2)
                }
            ],
            "isError": False
        }
    except Exception as error:
        return {
            "content": [
                {"type": "text", "text": str(error)}
            ],
            "isError": True
        }
