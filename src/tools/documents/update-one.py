# File: tools/update_one_tool.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def updateOne(collection: str, filter: dict, update: dict) -> dict:
    """
    Update a single document in a MongoDB collection.

    Args:
        collection: Name of the collection
        filter: Filter to identify document
        update: Update operations to apply

    Returns:
        A dictionary with the update result.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")
        if not isinstance(filter, dict):
            raise ValueError("Filter must be a dictionary")
        if not isinstance(update, dict):
            raise ValueError("Update must be a dictionary")

        result = await db[collection].update_one(filter, update)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "matched": result.matched_count,
                        "modified": result.modified_count,
                        "upsertedId": str(result.upserted_id) if result.upserted_id else None
                    }, indent=2)
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