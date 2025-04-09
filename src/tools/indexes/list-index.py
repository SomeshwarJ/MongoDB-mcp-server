# File: tools/list_indexes_tool.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def indexes(collection: str) -> dict:
    """
    List indexes for a MongoDB collection.

    Args:
        collection: Name of the collection

    Returns:
        A dictionary with the list of index definitions.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")

        indexes = await db[collection].list_indexes().to_list(length=None)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(indexes, indent=2)
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