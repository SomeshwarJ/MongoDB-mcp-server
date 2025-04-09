# File: tools/find_tool.py

from mongodb.client import db
from mcp.server.fastmcp import mcp
import json

@mcp.tool()
async def find(collection: str, filter: dict = None, limit: int = 10, projection: dict = None) -> dict:
    """
    Query documents in a collection using MongoDB query syntax.

    Args:
        collection: Name of the collection to query
        filter: MongoDB query filter (default {})
        limit: Max number of documents to return (default 10, max 1000)
        projection: Fields to include/exclude (default {})

    Returns:
        A dictionary with the query results.
    """
    try:
        if not isinstance(collection, str):
            raise ValueError("Collection name must be a string")
        if filter is not None and not isinstance(filter, dict):
            raise ValueError("Filter must be a dictionary")
        if projection is not None and not isinstance(projection, dict):
            raise ValueError("Projection must be a dictionary")

        results = await db[collection].find(filter or {}).project(projection or {}).limit(min(limit or 10, 1000)).to_list(length=min(limit or 10, 1000))

        return {
            "content": [
                {"type": "text", "text": json.dumps(results, indent=2)}
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