# File: tools/list_collections.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def listCollections() -> dict:
    """
    List all available collections in the database.

    Returns:
        A dictionary containing the list of collections and their types.
    """
    try:
        collections_cursor = db.list_collections()
        collections = await collections_cursor.to_list(length=None)
        result = [
            {"name": c.get("name"), "type": c.get("type")} for c in collections
        ]

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
                {
                    "type": "text",
                    "text": str(error),
                }
            ],
            "isError": True,
        }