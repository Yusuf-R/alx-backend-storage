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
    doc_list: list = []
    for doc in mongo_collection.find():
        doc_list.append(doc)
    return doc_list
