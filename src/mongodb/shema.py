# File: tools/infer_schema.py

from typing import Any, Dict, List, Optional, Set, Union
from pymongo.collection import Collection

class MongoFieldSchema:
    def __init__(self, field: str, type_: str, is_required: bool, sub_fields: Optional[List['MongoFieldSchema']] = None):
        self.field = field
        self.type = type_
        self.is_required = is_required
        self.sub_fields = sub_fields

    def to_dict(self):
        return {
            "field": self.field,
            "type": self.type,
            "isRequired": self.is_required,
            "subFields": [sf.to_dict() for sf in self.sub_fields] if self.sub_fields else None,
        }

def infer_schema_from_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, (int, float, str, bool)):
        return type(value).__name__
    if hasattr(value, 'isoformat'):
        return "date"
    return "unknown"

def infer_schema_from_document(doc: Dict[str, Any], parent_path: str = "") -> List[MongoFieldSchema]:
    schema = []
    for key, value in doc.items():
        field_path = f"{parent_path}.{key}" if parent_path else key
        field_type = infer_schema_from_value(value)
        field = MongoFieldSchema(field_path, field_type, True)

        if field_type == "object":
            field.sub_fields = infer_schema_from_document(value, field_path)
        elif field_type == "array" and value and isinstance(value[0], dict):
            field.sub_fields = infer_schema_from_document(value[0], f"{field_path}[]")

        schema.append(field)
    return schema

async def build_collection_schema(collection: Collection, sample_size: int = 100) -> Dict[str, Any]:
    docs = await collection.find({}).limit(sample_size).to_list(length=sample_size)
    count = await collection.count_documents({})
    indexes = await collection.index_information()

    field_schemas: Dict[str, Set[str]] = {}
    required_fields: Set[str] = set()

    for doc in docs:
        doc_schema = infer_schema_from_document(doc)
        for field in doc_schema:
            if field.field not in field_schemas:
                field_schemas[field.field] = set()
            field_schemas[field.field].add(field.type)
            required_fields.add(field.field)

    for doc in docs:
        present_fields = set(doc.keys())
        for field in list(required_fields):
            if field.split(".")[0] not in present_fields:
                required_fields.discard(field)

    fields: List[MongoFieldSchema] = []
    for field, types in field_schemas.items():
        inferred_type = next(iter(types)) if len(types) == 1 else "|".join(types)
        fields.append(MongoFieldSchema(field, inferred_type, field in required_fields))

    for doc in docs:
        doc_schema = infer_schema_from_document(doc)
        for field_schema in doc_schema:
            if field_schema.sub_fields:
                for f in fields:
                    if f.field == field_schema.field and not f.sub_fields:
                        f.sub_fields = field_schema.sub_fields

    return {
        "collection": collection.name,
        "fields": [f.to_dict() for f in fields],
        "count": count,
        "indexes": list(indexes.values()),
    }
