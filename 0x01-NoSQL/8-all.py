#!/usr/bin/env python3
""" List of documents """


def list_all(mongo_collection) -> list:
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
    if mongo_collection.estimated_document_count() == 0:
        return []
    return list(mongo_collection.find())
