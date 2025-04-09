# File: tools/delete_one_tool.py

from mongodb.client import db
from tools.base.tool import BaseTool
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def deleteOne(collection: str, filter: dict) -> dict:
    """
    Delete a single document from a collection.

    Args:
        collection: Name of the collection
        filter: Filter to identify the document

    Returns:
        A dictionary with number of deleted documents.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")
        if not isinstance(filter, dict):
            raise ValueError("Filter must be a dictionary")

        result = await db[collection].delete_one(filter)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"deleted": result.deleted_count}, indent=2)
                }
            ],
            "isError": False
        }
    except Exception as error:
        return {
            "content": [
                {
                    "type": "text",
                    "text": str(error)
                }
            ],
            "isError": True
        }
