# File: tools/drop_index_tool.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def dropIndex(collection: str, indexName: str) -> dict:
    """
    Drop an index from a MongoDB collection.

    Args:
        collection: Name of the collection
        indexName: Name of the index to drop

    Returns:
        A dictionary with the drop index result.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")
        if not isinstance(indexName, str):
            raise ValueError("Index name must be a string")

        result = await db[collection].drop_index(indexName)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
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