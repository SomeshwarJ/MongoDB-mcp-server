# File: tools/base/tool.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class McpError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

class ErrorCode:
    InvalidRequest = "invalid_request"

ToolResponse = Dict[str, Any]
ToolParams = Dict[str, Any]

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def execute(self, params: ToolParams) -> ToolResponse:
        pass

    def validate_collection(self, collection: Any) -> str:
        if not isinstance(collection, str):
            raise McpError(ErrorCode.InvalidRequest, f"Collection name must be a string, got {type(collection).__name__}")
        return collection

    def validate_object(self, value: Any, name: str) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise McpError(ErrorCode.InvalidRequest, f"{name} must be an object")
        return value

    def handle_error(self, error: Any) -> ToolResponse:
        return {
            "content": [
                {
                    "type": "text",
                    "text": str(error)
                }
            ],
            "isError": True
        }
