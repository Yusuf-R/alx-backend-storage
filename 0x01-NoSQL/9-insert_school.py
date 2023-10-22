#!/usr/bin/env python3
""" Insert a document in Python"""
# Python function that inserts a new document in a collection based on kwargs:

# Prototype: def insert_school(mongo_collection, **kwargs):
# mongo_collection will be the pymongo collection object
# Returns the new _id


def insert_school(mongo_collection, **kwargs):
    """
    Insert a school document into a MongoDB collection.

    Args:
        mongo_collection: A MongoDB collection object.
        **kwargs: Keyword arguments representing
        the fields and values of the school document.

    Returns:
        The inserted ID of the school document.

    Raises:
        None.
    """
    obj = mongo_collection.insert_one(kwargs)
    return obj.inserted_id
