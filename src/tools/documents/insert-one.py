# File: tools/find_tool.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def insertOne(collection: str, document: dict) -> dict:
    """
    Insert a single document into a MongoDB collection.

    Args:
        collection: Name of the collection
        document: Document to insert

    Returns:
        A dictionary with insertion result.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")
        if not isinstance(document, dict):
            raise ValueError("Document must be a dictionary")

        result = await db[collection].insert_one(document)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "acknowledged": result.acknowledged,
                        "insertedId": str(result.inserted_id)
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
