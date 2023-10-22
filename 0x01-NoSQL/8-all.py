#!/usr/bin/env python3
"""
List all documents in a MongoDB collection.

Args:
    mongo_collection: A MongoDB collection object.

Returns:
    A list of documents in the collection.
    If the collection is empty, an empty list is returned.

Raises:
    None.
"""


def list_all(mongo_collection) -> list:
    if mongo_collection.estimated_document_count() == 0:
        return []
    return list(mongo_collection.find())
